movie-poster-bot/
├─ app/
│  ├─ __init__.py
│  ├─ config.py
│  ├─ main.py                 # FastAPI health + webhook entry
│  ├─ telegram_bot.py         # bot setup + commands
│  ├─ poster_formatter.py     # builds message text like your screenshots
│  ├─ services/
│  │   ├─ __init__.py
│  │   ├─ tmdb_service.py
│  │   ├─ omdb_service.py
│  │   ├─ anilist_service.py
│  │   ├─ aggregator.py
│  │   └─ utils.py
├─ requirements.txt
├─ Dockerfile
├─ Procfile
├─ koyeb.yaml
├─ .env.example
└─ README.md
