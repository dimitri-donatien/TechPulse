from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
import feedparser
from langchain_community.chat_models import ChatOpenAI
import os

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

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

# 🔹 Filtrage intelligent avec le modèle Ollama
KEYWORDS_TECH = [
    "devops", "ia", "solid.js", "vue.js", "react.js", "next.js", "rust", "javascript",
    "css", "typescript", "mongodb", "cybersecurity", "machine learning", "performance",
    "php", "laravel", "python", "flask", "fastapi", "django", "go", "node.js"
]

KEYWORDS_DESIGN = ["UI", "UX", "Figma", "Tailwind", "design trends", "no-code", "CSS", "typography"]

@CrewBase
class Techpulse():
	"""TechpulseBis crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	os.environ["OPENAI_API_KEY"] = "testapikey"

	ollama_model = ChatOpenAI(model="ollama/llama3.1", base_url="http://localhost:11434")
	
	def fetch_news(self, sources):
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
	
	def evaluate_relevance(self, articles, keywords):
		relevant_articles = []
		for article in articles:
			# Vérification si un mot-clé apparaît dans le titre ou le contenu
			if any(kw.lower() in (article["title"] + " " + article["content"]).lower() for kw in keywords):
				prompt = f"Titre: {article['title']}\nContenu: {article['content']}\nNote sur 10 ?"
				score = self.ollama_model.invoke(prompt)
				try:
					score = int(score.strip())
					if score >= 6:
						relevant_articles.append(article)
				except ValueError:
					continue  
		return relevant_articles
	
	def summarize_articles(self, articles):
		if not articles:
			return "Aucun article pertinent n'a été trouvé."
		text = "\n".join([f"{a['title']} - {a['url']}" for a in articles])
		prompt = f"Articles tech et web design récents :\n{text}\nFais un résumé concis."
		return self.ollama_model.invoke(prompt)

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools
	@agent
	def tech_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['tech_agent'],
			run=lambda: self.fetch_news(TECH_SOURCES),
			verbose=True
		)
	
	@agent
	def design_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['design_agent'],
			run=lambda: self.fetch_news(DESIGN_SOURCES),
			verbose=True
		)
	
	@agent
	def tech_filter_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['tech_filter_agent'],
			run=lambda: self.evaluate_relevance(self.fetch_news(TECH_SOURCES), KEYWORDS_TECH),
			verbose=True
		)
	
	@agent
	def design_filter_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['design_filter_agent'],
			run=lambda: self.evaluate_relevance(self.fetch_news(DESIGN_SOURCES), KEYWORDS_DESIGN),
			verbose=True
		)
	
	@agent
	def summary_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['summary_agent'],
			run=lambda: self.summarize_articles(
				self.evaluate_relevance(
					# Fusionne les articles des deux types de sources
					self.fetch_news(TECH_SOURCES) + self.fetch_news(DESIGN_SOURCES),
					# Utilise une liste combinée de mots-clés pour filtrer les articles
					KEYWORDS_TECH + KEYWORDS_DESIGN
				)
			),
			verbose=True
		)


	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
	@task
	def fetch_news(self) -> Task:
		return Task(
			config=self.tasks_config['fetch_news']
		)
	
	@task
	def fetch_design_news(self) -> Task:
		return Task(
			config=self.tasks_config['fetch_design_news']
		)
	
	@task
	def filter_tech_news(self) -> Task:
		return Task(
			config=self.tasks_config['filter_tech_news']
		)
	
	@task
	def filter_design_news(self) -> Task:
		return Task(
			config=self.tasks_config['filter_design_news']
		)
	
	@task
	def summarize_news(self) -> Task:
		return Task(
			config=self.tasks_config['summarize_news'],
			output_file="summary.md"
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the TechpulseBis crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
