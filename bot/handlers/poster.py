from typing import Any, Dict, List
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from telegram.ext import ContextTypes
from ..services.aggregator import get_metadata_and_images
from ..utils.helpers import extract_year_from_query, build_caption_box


SESSION_KEY = "poster_sessions"


def _get_sessions(context: ContextTypes.DEFAULT_TYPE) -> Dict[str, Any]:
    if SESSION_KEY not in context.user_data:
        context.user_data[SESSION_KEY] = {}
    return context.user_data[SESSION_KEY]


async def p_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.text:
        return
    args = update.message.text.split(" ", 1)
    if len(args) < 2 or not args[1].strip():
        await update.message.reply_text(
            "Send like: /p naruto | /p iron man 2012",
            parse_mode="Markdown",
        )
        return

    query_text = args[1]
    title, year = extract_year_from_query(query_text)

    await update.message.chat.send_chat_action("upload_photo")
    meta = await get_metadata_and_images(title, year)
    if not meta or not meta.get("images"):
        await update.message.reply_text("No posters found for your query.")
        return

    images: List[Dict[str, Any]] = meta["images"]
    sessions = _get_sessions(context)
    session_id = str(update.message.message_id)
    sessions[session_id] = {
        "meta": meta,
        "index": 0,
        "total": len(images),
        "message_id": None,
    }

    first = images[0]
    caption = build_caption_box(
        meta["title"],
        meta["year"],
        meta["rating"],
        meta["content_type"],
        meta["overview"],
        meta["genres"],
        audio_info=None,
    )
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("⬅ Prev", callback_data=f"poster:{session_id}:prev"),
                InlineKeyboardButton("Next ➡", callback_data=f"poster:{session_id}:next"),
            ],
            [InlineKeyboardButton("Select 🎯", callback_data=f"poster:{session_id}:select")],
        ]
    )
    msg = await update.message.reply_photo(
        photo=first["url"],
        caption=caption,
        reply_markup=keyboard,
    )
    sessions[session_id]["message_id"] = msg.message_id


async def poster_pagination_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.callback_query:
        return
    query = update.callback_query
    await query.answer()
    data = query.data or ""
    if not data.startswith("poster:"):
        return
    _, session_id, action = data.split(":", 2)
    sessions = _get_sessions(context)
    session = sessions.get(session_id)
    if not session:
        await query.edit_message_caption(caption="Session expired. Please use /p again.")
        return

    meta = session["meta"]
    images: List[Dict[str, Any]] = meta["images"]
    idx = session["index"]
    total = session["total"]

    if action == "next":
        idx = (idx + 1) % total
    elif action == "prev":
        idx = (idx - 1) % total
    elif action == "select":
        final = images[idx]
        caption = build_caption_box(
            meta["title"],
            meta["year"],
            meta["rating"],
            meta["content_type"],
            meta["overview"],
            meta["genres"],
            audio_info=None,
        )
        await query.message.reply_photo(photo=final["url"], caption=caption)
        return

    session["index"] = idx
    new_img = images[idx]
    caption = build_caption_box(
        meta["title"],
        meta["year"],
        meta["rating"],
        meta["content_type"],
        meta["overview"],
        meta["genres"],
        audio_info=None,
    )
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("⬅ Prev", callback_data=f"poster:{session_id}:prev"),
                InlineKeyboardButton("Next ➡", callback_data=f"poster:{session_id}:next"),
            ],
            [InlineKeyboardButton("Select 🎯", callback_data=f"poster:{session_id}:select")],
        ]
    )
    media = InputMediaPhoto(media=new_img["url"], caption=caption)
    await query.message.edit_media(media=media, reply_markup=keyboard)
