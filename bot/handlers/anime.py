from telegram import Update
from telegram.ext import ContextTypes, CommandHandler


async def anime_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    txt = (
        "🎌 Anime search tips:
"
        "- Use `/p naruto`
"
        "- Use `/p attack on titan`
"
        "- Add year if needed, e.g. `/p one piece 1999`."
    )
    await update.message.reply_text(txt)


async def donghua_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    txt = (
        "🐉 Donghua (Chinese animation):
"
        "Try `/p soul land` or `/p heaven official blessing` to view posters."
    )
    await update.message.reply_text(txt)


async def kdrama_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    txt = (
        "💠 K-Drama tips:
"
        "Examples: `/p crash landing on you`, `/p goblin`, `/p vincenzo`."
    )
    await update.message.reply_text(txt)


async def webseries_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    txt = (
        "🌐 Web series search:
"
        "Use `/p money heist`, `/p dark`, `/p the boys`, etc."
    )
    await update.message.reply_text(txt)


async def manga_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    txt = (
        "📚 Manga posters are approximated via anime / art sources.
"
        "Try `/p tokyo ghoul`, `/p demon slayer`, `/p chainsaw man`."
    )
    await update.message.reply_text(txt)


async def airing_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    txt = (
        "📅 Airing schedule is approximated, use TMDB / external trackers.
"
        "You can still use `/p <title>` for latest key visuals."
    )
    await update.message.reply_text(txt)


async def schedule_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    txt = (
        "🗓 Weekly schedule is not region-accurate in this bot.
"
        "Use `/p <anime name>` to view posters and visuals."
    )
    await update.message.reply_text(txt)


async def character_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    txt = (
        "👤 Character posters:
"
        "Use `/p naruto uzumaki`, `/p tony stark`, `/p levi ackerman`."
    )
    await update.message.reply_text(txt)
