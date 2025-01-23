import asyncio
from pathlib import Path

from bot_config import bot, dp
from handlers import router
from loguru import logger

dp.include_router(router)

BASE_DIR = Path(__file__).resolve().parent.parent

logger.remove()
logger.add(
    f"{BASE_DIR}/logs.log",
    rotation="1000 MB",
    retention="90 days",
    format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {file}:{line} | {message}",
    level="DEBUG",
    catch=True,
)


@logger.catch
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:

        print(
            """
                -----------------------------------
                Я запустился!!!
                -----------------------------------
              """
        )
        asyncio.run(main())

        logger.info("Start")

    except (KeyboardInterrupt, SystemExit):
        logger.warning("Interrupt!")
