from crewai import Agent, Task, Crew
import requests
import feedparser
from langchain.llms import Ollama
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from supabase import create_client

# 🛠️ Connexion Supabase
SUPABASE_URL = "https://xyzcompany.supabase.co"
SUPABASE_KEY = "TON_CLE_API"
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
                "content": entry.summary if hasattr(entry, 'summary') else ""
            })
    return articles

# 🔹 Détection tendances Twitter / Reddit
def get_twitter_shares(url):
    return 10  # Simulé

def get_reddit_upvotes(url):
    return 5  # Simulé

def enrich_articles_with_trends(articles):
    for article in articles:
        article["twitter_shares"] = get_twitter_shares(article["url"])
        article["reddit_upvotes"] = get_reddit_upvotes(article["url"])
    return articles

# 🔹 Filtrage intelligent
ollama_model = Ollama(model="mistral")

KEYWORDS_TECH = [
    "devops", "ia", "solid.js", "vue.js", "react.js", "next.js", "rust", "javascript",
    "css", "typescript", "mongodb", "cybersecurity", "machine learning", "performance",
    "php", "laravel", "python", "flask", "fastapi", "django", "go", "node.js"
]

KEYWORDS_DESIGN = ["UI", "UX", "Figma", "Tailwind", "design trends", "no-code", "CSS", "typography"]

def evaluate_relevance(articles, keywords):
    relevant_articles = []
    for article in articles:
        if any(kw.lower() in (article["title"] + " " + article["content"]).lower() for kw in keywords):
            prompt = f"Titre: {article['title']}\nContenu: {article['content']}\nNote sur 10 ?"
            score = ollama_model.predict(prompt)
            try:
                score = int(score.strip())
                if score >= 6:
                    relevant_articles.append(article)
            except ValueError:
                continue  
    return relevant_articles

# 🔹 Synthèse AI
def summarize_articles(articles):
    text = "\n".join([f"{a['title']} - {a['url']}" for a in articles])
    prompt = f"Articles tech et web design récents :\n{text}\nFais un résumé concis."
    return ollama_model.predict(prompt)

# 🔹 Stockage dans Notion
NOTION_API_KEY = "TON_NOTION_API_KEY"
NOTION_DATABASE_ID = "TON_DATABASE_ID"

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

# 🔹 Notification Email
def send_email(summary):
    sender_email = "tonemail@gmail.com"
    receiver_email = "tonemaildestinataire@gmail.com"
    password = "TON_MOT_DE_PASSE_APPLICATION"

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = "🚀 Veille Tech & Web Design - Résumé du jour"

    html_content = f"""
    <html>
        <body>
            <h2>🚀 Résumé de ta veille tech & design</h2>
            <ul>
                {''.join([f'<li><a href="{a["url"]}">{a["title"]}</a></li>' for a in summary])}
            </ul>
        </body>
    </html>
    """
    msg.attach(MIMEText(html_content, "html"))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()

# 🔹 Notification Discord
def send_to_discord(summary):
    webhook_url = "https://discord.com/api/webhooks/TON_WEBHOOK"
    message = "**🚀 Veille Tech & Web Design - Résumé du jour**\n\n" + "\n".join([f"🔹 **[{a['title']}]({a['url']})**" for a in summary])
    requests.post(webhook_url, json={"content": message})

# 🚀 Agents CrewAI
tech_agent = Agent("Tech Watcher", lambda: fetch_news(TECH_SOURCES))
design_agent = Agent("Web Design Watcher", lambda: fetch_news(DESIGN_SOURCES))

tech_filter_agent = Agent("Curateur Tech", lambda: evaluate_relevance(fetch_news(TECH_SOURCES), KEYWORDS_TECH))
design_filter_agent = Agent("Curateur Web Design", lambda: evaluate_relevance(fetch_news(DESIGN_SOURCES), KEYWORDS_DESIGN))

summary_agent = Agent("Synthétiseur", summarize_articles)

notifier_agent = Agent("Notifier", lambda: [send_email(summary_agent.run()), send_to_discord(summary_agent.run()), save_to_notion(summary_agent.run())])

# 🚀 CrewAI Workflow
crew = Crew(
    agents=[tech_agent, design_agent, tech_filter_agent, design_filter_agent, summary_agent, notifier_agent],
    tasks=[
        Task("Récupérer les news Tech", tech_agent),
        Task("Récupérer les news Web Design", design_agent),
        Task("Filtrer les articles Tech", tech_filter_agent),
        Task("Filtrer les articles Web Design", design_filter_agent),
        Task("Synthétiser les articles pertinents", summary_agent),
        Task("Notifier par Email & Discord", notifier_agent)
    ]
)

crew.kickoff()
