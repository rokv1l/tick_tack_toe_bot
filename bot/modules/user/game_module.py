from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    CommandHandler,
    CallbackContext,
    ConversationHandler,
    CallbackQueryHandler,
)
from loguru import logger

import config
from . import states
from config import user_messages


async def game_entry_point_callback(update: Update, context: CallbackContext) -> None:
    config.game_queue.put(update.effective_chat.id)
    await update.effective_chat.send_message(
        user_messages["game_entry_point_callback_0"]
    )
    return states.MAKE_A_MOVE


async def send_table(update: Update, context: CallbackContext) -> None:
    tg_id = update.effective_chat.id
    game = context.bot_data[tg_id][0]
    active_keyboard = []
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
        active_keyboard.append(keys_row)
    not_active_keyboard = []
    for row_num, row in enumerate(game.table):
        keys_row = []
        for elem_num, elem in enumerate(row):
            if elem is None:
                text = "ㅤ"
                data = "Z"
            elif elem == 0:
                text = "0"
                data = "Z"
            else:
                text = "X"
                data = "Z"
            keys_row.append(InlineKeyboardButton(text, callback_data=data))
        not_active_keyboard.append(keys_row)
    if game.active_player == game.player_2:
        await update.get_bot().edit_message_text(
            chat_id=game.player_1,
            message_id=context.bot_data[tg_id][1],
            text="Ваш ход",
            reply_markup=InlineKeyboardMarkup(active_keyboard),
        )
        await update.get_bot().edit_message_text(
            chat_id=game.player_2,
            message_id=context.bot_data[tg_id][2],
            text="Ход аппонента",
            reply_markup=InlineKeyboardMarkup(not_active_keyboard),
        )
        game.active_player = game.player_1
    elif game.active_player == game.player_1:
        await update.get_bot().edit_message_text(
            chat_id=game.player_1,
            message_id=context.bot_data[tg_id][1],
            text="Ход аппонента",
            reply_markup=InlineKeyboardMarkup(not_active_keyboard),
        )
        await update.get_bot().edit_message_text(
            chat_id=game.player_2,
            message_id=context.bot_data[tg_id][2],
            text="Ваш ход",
            reply_markup=InlineKeyboardMarkup(active_keyboard),
        )
        game.active_player = game.player_2


async def send_end_message(update: Update, context: CallbackContext) -> None:
    tg_id = update.effective_chat.id
    game = context.bot_data[tg_id][0]
    if game.active_player == game.player_1:
        await update.get_bot().edit_message_text(
            chat_id=game.player_1,
            message_id=context.bot_data[tg_id][1],
            text="Поздравляю, вы победили"
        )
        await update.get_bot().edit_message_text(
            chat_id=game.player_2,
            message_id=context.bot_data[tg_id][2],
            text="К сожалению вы проиграли"
        )
    else:
        await update.get_bot().edit_message_text(
            chat_id=game.player_2,
            message_id=context.bot_data[tg_id][2],
            text="Поздравляю, вы победили"
        )
        await update.get_bot().edit_message_text(
            chat_id=game.player_1,
            message_id=context.bot_data[tg_id][1],
            text="К сожалению вы проиграли"
        )
    del context.bot_data[game.player_1]
    del context.bot_data[game.player_2]


async def make_a_move_callback(update: Update, context: CallbackContext) -> None:
    tg_id = update.effective_chat.id
    game = context.bot_data[tg_id][0]
    if game.active_player != tg_id:
        return
    data = update.callback_query.data
    row_num, elem_num = data.split("_")
    if tg_id == game.player_1:
        game.table[int(row_num)][int(elem_num)] = 0
    else:
        game.table[int(row_num)][int(elem_num)] = 1
    is_win = game.check_win_condition()
    if is_win:
        await send_end_message(update, context)
        return ConversationHandler.END
    else:
        await send_table(update, context)


game_handler = ConversationHandler(
    entry_points=[
        CommandHandler("play", game_entry_point_callback),
    ],
    states={
        states.MAKE_A_MOVE: [CallbackQueryHandler(make_a_move_callback, pattern=r'\d_\d')],
    },
    fallbacks=[],
    allow_reentry=True
)
