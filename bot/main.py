import asyncio
import logging
from telegram.ext import (
    Application,
    CommandHandler,
)
from .config import config
from .handlers.poster import p_command
from .handlers.movies import (
    start,
    movies_command,
    tvshows_command,
    recommend_command,
    trendingmv_command,
    trendingtv_command,
    collection_command,
)
from .handlers.anime import (
    anime_command,
    donghua_command,
    kdrama_command,
    webseries_command,
    manga_command,
    airing_command,
    schedule_command,
    character_command,
)
from .handlers.callbacks import register_callbacks

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def main() -> None:
    application = (
        Application.builder()
        .token(config.BOT_TOKEN)
        .concurrent_updates(True)
        .build()
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("movies", movies_command))
    application.add_handler(CommandHandler("tvshows", tvshows_command))
    application.add_handler(CommandHandler("recommend", recommend_command))
    application.add_handler(CommandHandler("trendingmv", trendingmv_command))
    application.add_handler(CommandHandler("trendingtv", trendingtv_command))
    application.add_handler(CommandHandler("collection", collection_command))

    application.add_handler(CommandHandler("anime", anime_command))
    application.add_handler(CommandHandler("donghua", donghua_command))
    application.add_handler(CommandHandler("kdrama", kdrama_command))
    application.add_handler(CommandHandler("webseries", webseries_command))
    application.add_handler(CommandHandler("manga", manga_command))
    application.add_handler(CommandHandler("airing", airing_command))
    application.add_handler(CommandHandler("schedule", schedule_command))
    application.add_handler(CommandHandler("character", character_command))

    application.add_handler(CommandHandler("p", p_command))

    register_callbacks(application)

    logger.info("Starting bot polling...")
    await application.run_polling(close_loop=False)


if __name__ == "__main__":
    asyncio.run(main())
