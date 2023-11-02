from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from loguru import logger

import config
from config import user_messages
from src.telegram_api import app

from modules.game_engine.engine import GameEngine


async def find_game(_):
    if config.game_queue.qsize() >= 2:
        player_1 = config.game_queue.get_nowait()
        player_2 = config.game_queue.get_nowait()
        game = GameEngine(player_1, player_2)
        keyboard = []
        logger.info(game.table)
        for row_num, row in enumerate(game.table):
            keys_row = []
            for elem_num, elem in enumerate(row):
                if elem is None:
                    text = "ㅤ"
                    data = f"{row_num}_{elem_num}"
                elif elem == 0:
                    text = data = "0"
                else:
                    text = data = "X"
                keys_row.append(InlineKeyboardButton(text, callback_data=data))
            keyboard.append(keys_row)
        message_p1 = await app.bot.send_message(
            chat_id=player_1,
            text="Ваш ход",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        message_p2 = await app.bot.send_message(
            chat_id=player_2,
            text="Ход соперника",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        app.bot_data[player_1] = app.bot_data[player_2] = [game, message_p1.message_id, message_p2.message_id]
