from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = "6429632184:AAFdr_IJ-srecePv6x6kHPC3xUPPH5zlO_M"

waiting_player = None
games = {}


def start(update, context):
    global waiting_player

    user = update.message.from_user

    if waiting_player is None:
        waiting_player = user
        update.message.reply_text("Ожидание другого игрока...")
    else:
        games[(waiting_player.id, user.id)] = {
            "board": [["_", "_", "_"], ["_", "_", "_"], ["_", "_", "_"]],
            "current_player": waiting_player.id,
        }
        context.bot.send_message(waiting_player.id, "Игра началась!")
        context.bot.send_message(user.id, "Игра началась!")
        show_board(waiting_player.id, context)
        show_board(user.id, context)
        waiting_player = None


def show_board(user_id, context):
    board = games[get_game_key(user_id)]["board"]
    keyboard = []
    for i, row in enumerate(board):
        row_btns = []
        for j, cell in enumerate(row):
            row_btns.append(InlineKeyboardButton(cell, callback_data=f"cell_{i}_{j}"))
        keyboard.append(row_btns)

    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(user_id, "Делайте ваш ход:", reply_markup=reply_markup)


def get_game_key(user_id):
    for players, game in games.items():
        if user_id in players:
            return players
    return None


def cell_callback(update, context):
    user_id = update.callback_query.from_user.id
    game_key = get_game_key(user_id)

    if game_key is None:
        update.callback_query.answer("Вы не в игре!")
        return

    if games[game_key]["current_player"] != user_id:
        update.callback_query.answer("Сейчас не ваш ход!")
        return

    _, i, j = update.callback_query.data.split("_")
    i, j = int(i), int(int(j))

    board = games[game_key]["board"]

    if board[i][j] != "_":
        update.callback_query.answer("Эта ячейка уже занята!")
        return

    board[i][j] = "X" if user_id == game_key[0] else "O"

    if check_win(board, i, j):
        context.bot.send_message(
            game_key[0], "Вы победили!" if user_id == game_key[0] else "Вы проиграли!"
        )
        context.bot.send_message(
            game_key[1], "Вы победили!" if user_id == game_key[1] else "Вы проиграли!"
        )
        del games[game_key]
        return

    if check_draw(board):
        context.bot.send_message(game_key[0], "Ничья!")
        context.bot.send_message(game_key[1], "Ничья!")
        del games[game_key]
        return

    games[game_key]["current_player"] = (
        game_key[0] if user_id == game_key[1] else game_key[1]
    )
    show_board(game_key[0], context)
    show_board(game_key[1], context)


def check_win(board, i, j):
    player = board[i][j]
    return (
        all([cell == player for cell in board[i]])
        or all([board[row][j] == player for row in range(3)])
        or (i == j and all([board[d][d] == player for d in range(3)]))
        or (i + j == 2 and all([board[d][2 - d] == player for d in range(3)]))
    )


def check_draw(board):
    return all(cell != "_" for row in board for cell in row)


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(cell_callback, pattern="^cell_"))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
