from crewai import Agent, Task, Crew
import requests
import feedparser
from langchain_community.chat_models import ChatOpenAI
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from supabase import create_client
import os
from dotenv import load_dotenv

# Chargement des variables d'environnement
load_dotenv()

# 🛠️ Connexion Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# 🔹 Sources Tech & Web Design
TECH_SOURCES = [
    "https://news.ycombinator.com/rss",
    "https://dev.to/feed",
    "https://www.journaldunet.com/rss",
    "https://www.zdnet.fr/feeds/rss/actualites.xml"
]

DESIGN_SOURCES = [
    "https://www.smashingmagazine.com/feed/",
    "https://www.awwwards.com/blog/feed/",
    "https://css-tricks.com/feed/"
]

# 🔹 Récupération des articles
def fetch_news(sources):
    articles = []
    for source in sources:
        feed = feedparser.parse(source)
        for entry in feed.entries[:5]:
            articles.append({
                "title": entry.title,
                "url": entry.link,
                "content": entry.summary if hasattr(entry, "summary") else ""
            })
    return articles

# 🔹 Détection tendances Twitter / Reddit (simulation)
def get_twitter_shares(url):
    return 10  # Simulé

def get_reddit_upvotes(url):
    return 5  # Simulé

def enrich_articles_with_trends(articles):
    for article in articles:
        article["twitter_shares"] = get_twitter_shares(article["url"])
        article["reddit_upvotes"] = get_reddit_upvotes(article["url"])
    return articles

# 🔹 Définition du modèle OpenAI (avec clé API factice pour tests)
os.environ["OPENAI_API_KEY"] = "testapikey"

# 🔹 Instanciation du modèle local (ici via ChatOpenAI)
ollama_model = ChatOpenAI(model="ollama/mistral", base_url="http://localhost:11434", temperature=0.2)

# 🔹 Filtrage intelligent avec le modèle Ollama
KEYWORDS_TECH = [
    "devops", "ia", "solid.js", "vue.js", "react.js", "next.js", "rust", "javascript",
    "css", "typescript", "mongodb", "cybersecurity", "machine learning", "performance",
    "php", "laravel", "python", "flask", "fastapi", "django", "go", "node.js"
]

KEYWORDS_DESIGN = ["UI", "UX", "Figma", "Tailwind", "design trends", "no-code", "CSS", "typography"]

def evaluate_relevance(articles, keywords):
    relevant_articles = []
    for article in articles:
        # Vérification si un mot-clé apparaît dans le titre ou le contenu
        if any(kw.lower() in (article["title"] + " " + article["content"]).lower() for kw in keywords):
            prompt = f"Titre: {article['title']}\nContenu: {article['content']}\nNote sur 10 ?"
            score = ollama_model.invoke(prompt)
            try:
                score = int(score.strip())
                if score >= 6:
                    relevant_articles.append(article)
            except ValueError:
                continue  
    return relevant_articles

# 🔹 Synthèse AI des articles (renvoie un résumé textuel)
def summarize_articles(articles):
    if not articles:
        return "Aucun article pertinent n'a été trouvé."
    text = "\n".join([f"{a['title']} - {a['url']}" for a in articles])
    prompt = f"Articles tech et web design récents :\n{text}\nFais un résumé concis."
    return ollama_model.invoke(prompt)

# 🔹 Stockage dans Notion
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
def save_to_notion(articles):
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    for article in articles:
        data = {
            "parent": {"database_id": NOTION_DATABASE_ID},
            "properties": {
                "Titre": {"title": [{"text": {"content": article["title"]}}]},
                "URL": {"url": article["url"]},
                "Popularité": {"number": article.get("twitter_shares", 0) + article.get("reddit_upvotes", 0)}
            }
        }
        requests.post("https://api.notion.com/v1/pages", headers=headers, json=data)

# 🔹 Notification Email (utilise les variables SMTP_EMAIL, SMTP_PASSWORD et RECEIVER_EMAIL)
def send_email(articles):
    sender_email = os.getenv("SMTP_EMAIL")
    receiver_email = os.getenv("RECEIVER_EMAIL")
    password = os.getenv("SMTP_PASSWORD")
    
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = "🚀 Veille Tech & Web Design - Résumé du jour"
    
    # Construit la liste des articles sous forme de liens
    article_links = "".join([f'<li><a href="{a["url"]}">{a["title"]}</a></li>' for a in articles])
    html_content = f"""
    <html>
        <body>
            <h2>🚀 Résumé de ta veille tech & design</h2>
            <ul>{article_links}</ul>
        </body>
    </html>
    """
    msg.attach(MIMEText(html_content, "html"))
    
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("Email envoyé avec succès.")
    except Exception as e:
        print("Erreur lors de l'envoi de l'email :", e)

# 🔹 Notification Discord
def send_to_discord(articles):
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        print("Webhook Discord non configuré.")
        return
    message = "**🚀 Veille Tech & Web Design - Résumé du jour**\n\n" + "\n".join(
        [f"🔹 **[{a['title']}]({a['url']})**" for a in articles]
    )
    try:
        response = requests.post(webhook_url, json={"content": message})
        if response.status_code == 200:
            print("Notification Discord envoyée.")
        else:
            print("Erreur Discord:", response.text)
    except Exception as e:
        print("Erreur lors de l'envoi à Discord :", e)

# 🔹 Création des agents avec les champs requis
tech_agent = Agent(
    name="Tech Watcher",
    role="Récupération des news Tech",
    goal="Collecter les dernières news tech à partir des sources définies",
    backstory="Agent dédié à la récupération d'articles tech.",
    run=lambda: fetch_news(TECH_SOURCES),
    llm=ollama_model
)

design_agent = Agent(
    name="Web Design Watcher",
    role="Récupération des news Web Design",
    goal="Collecter les dernières news web design à partir des sources définies",
    backstory="Agent dédié à la récupération d'articles web design.",
    run=lambda: fetch_news(DESIGN_SOURCES),
    llm=ollama_model
)

tech_filter_agent = Agent(
    name="Curateur Tech",
    role="Filtrage des articles tech",
    goal="Évaluer la pertinence des articles tech en fonction de mots-clés",
    backstory="Agent qui filtre les articles tech selon des critères de pertinence.",
    run=lambda: evaluate_relevance(fetch_news(TECH_SOURCES), KEYWORDS_TECH),
    llm=ollama_model
)

design_filter_agent = Agent(
    name="Curateur Web Design",
    role="Filtrage des articles web design",
    goal="Évaluer la pertinence des articles web design en fonction de mots-clés",
    backstory="Agent qui filtre les articles web design selon des critères de pertinence.",
    run=lambda: evaluate_relevance(fetch_news(DESIGN_SOURCES), KEYWORDS_DESIGN),
    llm=ollama_model
)

summary_agent = Agent(
    name="Synthétiseur",
    role="Synthèse des articles",
    goal="Créer un résumé concis des articles récupérés",
    backstory="Agent qui synthétise les informations clés des articles pertinents.",
    run=summarize_articles,
    llm=ollama_model
)

notifier_agent = Agent(
    name="Notifier",
    role="Notification et stockage",
    goal="Notifier par email et Discord et sauvegarder dans Notion",
    backstory="Agent qui gère l'envoi de notifications et le stockage des articles.",
    run=lambda: [
        send_email(summary_agent.run()),
        send_to_discord(summary_agent.run()),
        save_to_notion(summary_agent.run())
    ],
    llm=ollama_model
)

# 🔹 Définition des tâches avec les champs requis et configuration du Crew avec notre LLM personnalisé
crew = Crew(
    agents=[tech_agent, design_agent, tech_filter_agent, design_filter_agent, summary_agent, notifier_agent],
    tasks=[
        Task(
            name="Récupérer les news Tech",
            agent=tech_agent,
            description="Collecte les dernières news tech à partir des sources prédéfinies",
            expected_output="Liste d'articles tech"
        ),
        Task(
            name="Récupérer les news Web Design",
            agent=design_agent,
            description="Collecte les dernières news web design à partir des sources prédéfinies",
            expected_output="Liste d'articles web design"
        ),
        Task(
            name="Filtrer les articles Tech",
            agent=tech_filter_agent,
            description="Filtre et évalue la pertinence des articles tech en fonction de mots-clés",
            expected_output="Articles tech pertinents"
        ),
        Task(
            name="Filtrer les articles Web Design",
            agent=design_filter_agent,
            description="Filtre et évalue la pertinence des articles web design en fonction de mots-clés",
            expected_output="Articles web design pertinents"
        ),
        Task(
            name="Synthétiser les articles pertinents",
            agent=summary_agent,
            description="Synthétise les articles filtrés en un résumé concis",
            expected_output="Résumé concis"
        ),
        Task(
            name="Notifier par Email & Discord",
            agent=notifier_agent,
            description="Envoie le résumé par email et Discord puis sauvegarde les articles dans Notion",
            expected_output="Notification envoyée et articles sauvegardés"
        )
    ]
)

if __name__ == "__main__":
    # Lancement du workflow
    crew.kickoff()