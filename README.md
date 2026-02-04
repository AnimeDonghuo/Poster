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
