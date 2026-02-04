from telegram.ext import Application
from .poster import poster_pagination_callback


def register_callbacks(app: Application) -> None:
    app.add_handler(poster_pagination_callback_handler())


def poster_pagination_callback_handler():
    from telegram.ext import CallbackQueryHandler

    return CallbackQueryHandler(poster_pagination_callback, pattern=r"^poster:")
