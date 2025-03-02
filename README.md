# 🚀 TechPulse - Veille intelligente Tech & Web Design  

![CI/CD Workflow](https://github.com/ton-compte/techpulse/actions/workflows/ci-cd.yml/badge.svg)
![Docker Image](https://img.shields.io/badge/Docker-GHCR-blue?logo=docker)
![Docker Pulls](https://img.shields.io/docker/pulls/ton-compte/techpulse)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/ton-compte/techpulse)
![GitHub last commit](https://img.shields.io/github/last-commit/ton-compte/techpulse)
![GitHub issues](https://img.shields.io/github/issues/ton-compte/techpulse)
![GitHub pull requests](https://img.shields.io/github/issues-pr/ton-compte/techpulse)
![GitHub license](https://img.shields.io/github/license/ton-compte/techpulse)
![GitHub stars](https://img.shields.io/github/stars/ton-compte/techpulse?style=social)
![GitHub top language](https://img.shields.io/github/languages/top/ton-compte/techpulse)

**TechPulse** est un assistant **IA open-source** qui automatise la **veille technologique et web design**.  
Il récupère, filtre et résume les tendances Tech & Web Design en utilisant **CrewAI + Ollama**, puis les notifie via **Discord, Email et Notion**.  

![TechPulse Banner](https://user-images.githubusercontent.com/xxxx/banner.png) *(Ajoute un vrai visuel ici !)*  

---

## 📌 Fonctionnalités

✅ **Scraping intelligent** : Récupère des articles depuis **Hacker News, Dev.to, Awwwards, Smashing Magazine…**  
✅ **Filtrage AI** : Classe les articles avec **Ollama (Mistral)** selon tes **intérêts (DevOps, IA, Web Design, etc.)**  
✅ **Détection de tendances** : Analyse la popularité des articles via **Twitter & Reddit**  
✅ **Synthèse automatique** : Résume les meilleurs articles avec **un LLM local**  
✅ **Notifications** : Envoie un **email HTML, un message Discord formaté et archive les tendances sur Notion / Supabase**  
✅ **Automatisation** : Fonctionne en **tâche planifiée (Cron / GitHub Actions)**  

---

## 📸 Aperçu

📩 **Exemple d’email généré**  
*(Ajoute ici une capture d’écran d’un email généré avec les articles.)*  

💬 **Exemple de notification Discord**  
*(Ajoute ici une capture du message Discord généré.)*  

---

## 🚀 Installation & Configuration

### 1️⃣ Prérequis

- **Python 3.10+**
- **Ollama (Mistral) installé localement** ([Guide](https://ollama.ai/))
- **Créer un bot Discord & Webhook** ([Guide](https://discord.com/developers/docs/intro))
- **Un compte Notion API / Supabase** (facultatif)
- **Docker & Docker Compose** (facultatif)

### 2️⃣ Cloner le projet

```sh
git clone https://github.com/ton-compte/techpulse.git
cd techpulse
```

3️⃣ Installer les dépendances

```sh
pip install -r requirements.txt
```

4️⃣ Configurer les variables d’environnement

Crée un fichier .env et ajoute :

```sh
DISCORD_WEBHOOK_URL=ton_webhook_discord
SMTP_EMAIL=ton_email@gmail.com
SMTP_PASSWORD=ton_mot_de_passe_application
NOTION_API_KEY=ta_cle_notion
NOTION_DATABASE_ID=ton_id_notion
SUPABASE_URL=https://xyzcompany.supabase.co
SUPABASE_KEY=ta_cle_supabase
```

5️⃣ Lancer le script

```sh
python main.py
```

---

🔄 Déploiement avec Docker

📌 Lancer l’application avec Docker Compose

```sh
docker-compose up --build -d
```

📌 Voir les logs en direct

```sh
docker-compose logs -f
```

📌 Arrêter les conteneurs

```sh
docker-compose down
```

---

🕰️ Automatisation

Exécuter tous les jours avec un Cron Job
Ajoute cette ligne dans ton crontab -e :

```sh
0 0 * * * /usr/bin/python3 /home/ton_user/techpulse/main.py
```

(Exécution tous les jours à 9h)

Automatiser avec GitHub Actions

Ajoute un fichier .github/workflows/schedule.yml pour planifier l’exécution automatique.

---

📜 Contribution

🚀 Envie d’améliorer TechPulse ?

Forke le projet et propose des Pull Requests ! 🙌

🌱 Comment contribuer ?

Forker & Cloner le projet :

```sh
git clone https://github.com/votre-utilisateur/techpulse.git
cd techpulse
```

Créer une branche :

```sh
git checkout -b feature-nouvelle-fonction
```

Faire vos modifications et tester :

```sh
python main.py
```

Commit & Push :

```sh
git add .
git commit -m "Ajout de la fonctionnalité X"
git push origin feature-nouvelle-fonction
```

Ouvrir une Pull Request (PR) sur GitHub.

📌 Idées d’améliorations :

Ajouter un dashboard Web (Next.js)
Améliorer la pertinence AI (fine-tuning d’un modèle local)
Détection avancée des tendances Twitter / Reddit

---

📝 License

🔓 TechPulse est sous licence MIT – Utilisation et modifications libres.

---

💬 Contact

💻 Développé avec ❤️ par @tonpseudo
📧 Contact : tonemail@gmail.com