# 🚀 TechPulse - Veille intelligente Tech & Web Design  

<!-- ![CI/CD Workflow](https://github.com/dimitri-donatien/techpulse/actions/workflows/ci-cd.yml/badge.svg) -->
<!-- ![Docker Image](https://img.shields.io/badge/Docker-GHCR-blue?logo=docker) -->
<!-- ![Docker Pulls](https://img.shields.io/docker/pulls/dimitri-donatien/techpulse) -->
![GitHub release (latest by date)](https://img.shields.io/github/v/release/dimitri-donatien/techpulse)
![GitHub last commit](https://img.shields.io/github/last-commit/dimitri-donatien/techpulse)
![GitHub issues](https://img.shields.io/github/issues/dimitri-donatien/techpulse)
![GitHub pull requests](https://img.shields.io/github/issues-pr/dimitri-donatien/techpulse)
![GitHub license](https://img.shields.io/github/license/dimitri-donatien/techpulse)
![GitHub stars](https://img.shields.io/github/stars/dimitri-donatien/techpulse?style=social)

**TechPulse** est un assistant **IA open-source** qui automatise la **veille technologique et web design**.  
Il récupère, filtre et résume les tendances Tech & Web Design en utilisant **CrewAI + Ollama**, puis les notifie via **Discord, Email et Notion**.  

![TechPulse Banner](https://user-images.githubusercontent.com/xxxx/banner.png) *(Ajoute un vrai visuel ici !)*  

---

## 📸 Aperçu

📩 **Exemple d’email généré**  
*(Ajoute ici une capture d’écran d’un email généré avec les articles.)*  

💬 **Exemple de notification Discord**  
*(Ajoute ici une capture du message Discord généré.)*  

---

## 📌 Fonctionnalités

✅ **Scraping intelligent** : Récupère des articles depuis **Hacker News, Dev.to, Awwwards, Smashing Magazine…**  
✅ **Filtrage AI** : Classe les articles avec **Ollama (Mistral)** selon tes **intérêts (DevOps, IA, Web Design, etc.)**  
❌ **Détection de tendances** : Analyse la popularité des articles via **Twitter & Reddit**  
✅ **Synthèse automatique** : Résume les meilleurs articles avec **un LLM local**  
❌ **Notifications** : Envoie un **email HTML, un message Discord formaté et archive les tendances sur Notion / Supabase**  
❌ **Automatisation** : Fonctionne en **tâche planifiée (Cron / GitHub Actions)**  

---

## 📦 Technologies

- **Python** : Langage de programmation principal
- **Ollama (Mistral)** : IA pour le filtrage des articles ([Guide](https://ollama.ai/))
- **Discord Webhook** : Envoi de notifications ([Guide](https://discord.com/developers/docs/intro))
- **Notion API** : Stockage des tendances (In Progress) (facultatif)
- **Supabase** : Stockage des tendances (In Progress) (facultatif)
- **Docker** : Conteneurisation de l’application (In Progress) (facultatif)

---

## Achitecture dossier

```sh
techpulse/
├── .gitignore
├── knowledge/
├── pyproject.toml
├── README.md
├── .env
└── src/
    └── techpulse/
        ├── __init__.py
        ├── main.py
        ├── crew.py
        ├── tools/
        │   ├── custom_tool.py
        │   └── __init__.py
        └── config/
            ├── agents.yaml
            └── tasks.yaml
```

## Les fichiers essentiels

| File          | Purpose                                         |
|---------------|-------------------------------------------------|
| agents.yaml   | Define your AI agents and their roles           |
| tasks.yaml    | Set up agent tasks and workflows                |
| .env          | Store API keys and environment variables        |
| main.py       | Project entry point and execution flow          |
| crew.py       | Crew orchestration and coordination             |
| tools/        | Directory for custom agent tools                |
| knowledge/    | Directory for knowledge base and data storage   |

Pour plus d'information sur la configuration des fichiers, consultez la documentation [ici](https://docs.crewai.com/introduction).

---

> Commencez par éditer `agents.yaml` et `tasks.yaml` pour définir le comportement de votre équipe d’IA.

---

> Conservez les informations sensibles comme les clés API dans .env.

---

## 🚀 Installation & Configuration

### 1️⃣ Cloner le projet

```sh
git clone https://github.com/dimitri-donatien/techpulse.git
cd techpulse
```

### 2️⃣ Installer les dépendances

```sh
crewai install
```

### 3️⃣ Configurer les variables d’environnement

Crée un fichier .env et ajoute :

```sh
MODEL=ollama/Nom_Model
API_BASE=****************
DISCORD_WEBHOOK_URL=ton_webhook_discord
SMTP_EMAIL=ton_email@gmail.com
SMTP_PASSWORD=ton_mot_de_passe_application
NOTION_API_KEY=ta_cle_notion
NOTION_DATABASE_ID=ton_id_notion
SUPABASE_URL=https://xyzcompany.supabase.co
SUPABASE_KEY=ta_cle_supabase
```

### 4️⃣ Lancer le script

```sh
crewai run
```

### 5️⃣ Installer des packages supplémentaires

```sh
uv add <package-name>
```

---

## 🕰️ Automatisation

Exécuter tous les jours avec un Cron Job
Ajoute cette ligne dans ton crontab -e :

```sh
0 0 * * * /usr/bin/python3 /home/ton_user/techpulse/main.py
```

(Exécution tous les jours à 9h)

Automatiser avec GitHub Actions

Ajoute un fichier .github/workflows/schedule.yml pour planifier l’exécution automatique.

---

## 📝 License

🔓 TechPulse est sous licence MIT – Utilisation et modifications libres.

---

## 💬 Contact

💻 Développé avec ❤️ par [@dimitri-donatien](https://github.com/dimitri-donatien)

📧 Contact : <donatien.dim@gmail.com>
