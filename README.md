# Telegram Movie / Anime / Poster Bot

Async Telegram bot that fetches posters from TMDB, OMDb, IMDb CDN, FanArt-like sources, ThePosterDB, TVDB, AniDB, MAL CDN, AlphaCoders, Wallhaven, CineMaterial, MoviePosterDB, Wikimedia, Google Images, and Bing Images via scraping and aggregation.[web:9][web:1]

## Features

- `/p <query>` intelligent search (movie, TV, anime, donghua, manga, characters, collections).
- Inline pagination with Prev / Next / Select using edited media.[web:3]
- Rich caption box with title, year, rating, quality options, audio placeholder, genres, and synopsis.
- Helper commands for movies, TV shows, trending, anime, donghua, kdrama, webseries, manga, airing, schedule, character.

## Commands

- `/start` – Help and overview.
- `/p <query>` – Poster search.
- `/movies` – Popular / trending movies.
- `/tvshows` – Popular / trending TV shows.
- `/recommend` – Random trending movies.
- `/trendingmv` – Alias for `/movies`.
- `/trendingtv` – Alias for `/tvshows`.
- `/collection` – Collection hints.
- `/anime` – Anime usage hints.
- `/donghua` – Donghua hints.
- `/kdrama` – K-Drama hints.
- `/webseries` – Web series hints.
- `/manga` – Manga hints.
- `/airing` – Airing notes.
- `/schedule` – Schedule notes.
- `/character` – Character poster usage.

## Environment variables

Copy `.env.example` to `.env` (for local Docker) or configure in your platform.

```env
BOT_TOKEN=your_telegram_bot_token
TMDB_API_KEY=your_tmdb_api_key
OMDB_API_KEY=your_omdb_api_key
DEBUG=false

## Local Run

pip install -r requirements.txt
export BOT_TOKEN=...
export TMDB_API_KEY=...
export OMDB_API_KEY=...
python -m bot.main

## Heroku deployment

Create app:heroku create poster-botSet config vars:heroku config:set BOT_TOKEN=your_token
heroku config:set TMDB_API_KEY=your_tmdb_key
heroku config:set OMDB_API_KEY=your_omdb_key
heroku config:set DEBUG=falseDeploy:git init
git add .
git commit -m "Initial commit"
heroku git:remote -a poster-bot
git push heroku mainHeroku will run the worker defined in Procfile.

## Koyeb deployment
Push this repository to GitHub.In Koyeb dashboard,
 create a new service from GitHub, select this repo.
use Dockerfile build, instance type free.
Set environment variables:BOT_TOKENTMDB_API_KEYOMDB_API_KEYDEBUG=falseDeploy;
 the bot runs with polling.

Docker usageBuild and run with Docker:docker build -t poster-bot .
docker run --rm \
  -e BOT_TOKEN=your_token \
  -e TMDB_API_KEY=your_tmdb_key \
  -e OMDB_API_KEY=your_omdb_key \
  poster-botOr using Docker Compose:docker-compose up --buildThe bot uses long polling and does not expose HTTP ports.



***

Deployment steps summary [3][4]

- **Heroku**: Push repo, set `BOT_TOKEN`, `TMDB_API_KEY`, `OMDB_API_KEY`, ensure worker dyno is enabled; `Procfile` runs the bot via polling.[3]
- **Koyeb**: Create a container service from GitHub with `Dockerfile`, set environment variables in the dashboard, use free instance, deploy; polling works without webhooks.[4]
- **Docker**: Build the image, run with environment variables, or use `docker-compose.yml` for convenient local or server deployment.
