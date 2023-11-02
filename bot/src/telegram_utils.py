
from loguru import logger


async def delete_old_keyboard(context, chat_id):
    if context.user_data.get("msg_for_del_keys"):
        try:
            await context.bot.edit_message_text(
                text=context.user_data["msg_for_del_keys"].text,
                chat_id=chat_id,
                message_id=context.user_data["msg_for_del_keys"].message_id
            )
        except Exception:
            pass
        del context.user_data["msg_for_del_keys"]
