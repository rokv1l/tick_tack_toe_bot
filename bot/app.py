
import src.logger_config

from loguru import logger

from src.telegram_api import app, job_queue
from modules.errors_module import error_callback
from modules import user


if __name__ == "__main__":
    logger.info("Inializing complete, bot starting")
    app.add_handler(user.start_handler)
    app.add_handler(user.game_handler)
    job_queue.run_repeating(user.find_game, 5)
    app.add_error_handler(error_callback)
    app.run_polling()
