from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from ..services import tmdb
from ..utils.helpers import build_caption_box


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = (
        "🎬 Movie / Anime / Poster Bot

"
        "Commands:
"
        "/p <query> - Search posters
"
        "/movies - Popular movies
"
        "/tvshows - Popular TV shows
"
        "/trendingmv - Trending movies
"
        "/trendingtv - Trending TV shows
"
        "/recommend - Random picks
"
        "/collection - Collection hints
"
        "/anime /donghua /kdrama /webseries /manga /airing /schedule /character"
    )
    await update.message.reply_text(text)


async def movies_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    res = await tmdb.get_trending("movie", "day")
    if not res:
        await update.message.reply_text("No movies available right now.")
        return
    lines = []
    for i, item in enumerate(res[:10], start=1):
        title = item.get("title") or "Unknown"
        rating = item.get("vote_average") or "N/A"
        lines.append(f"{i}. {title} ({rating}/10)")
    await update.message.reply_text("🎬 Popular / Trending Movies:

" + "
".join(lines))


async def tvshows_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    res = await tmdb.get_trending("tv", "day")
    if not res:
        await update.message.reply_text("No TV shows available right now.")
        return
    lines = []
    for i, item in enumerate(res[:10], start=1):
        title = item.get("name") or "Unknown"
        rating = item.get("vote_average") or "N/A"
        lines.append(f"{i}. {title} ({rating}/10)")
    await update.message.reply_text("📺 Popular / Trending TV Shows:

" + "
".join(lines))


async def recommend_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    res = await tmdb.get_trending("movie", "week")
    if not res:
        await update.message.reply_text("No recommendations available.")
        return
    import random

    picks = random.sample(res, k=min(5, len(res)))
    text_lines = ["🎯 Recommendations:"]
    for i, item in enumerate(picks, start=1):
        title = item.get("title") or "Unknown"
        rating = item.get("vote_average") or "N/A"
        text_lines.append(f"{i}. {title} ({rating}/10)")
    await update.message.reply_text("
".join(text_lines))


async def trendingmv_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await movies_command(update, context)


async def trendingtv_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await tvshows_command(update, context)


async def collection_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    txt = (
        "📚 Collections / Franchises:
"
        "- Marvel Cinematic Universe
"
        "- DC Extended Universe
"
        "- Harry Potter Collection
"
        "- The Lord of the Rings

"
        "Use `/p <collection name>` to browse posters."
    )
    await update.message.reply_text(txt)
