import botCore
import parserCore

from aiogram import utils

from modules import adblocker, database, rating


async def send_post(message):
    if adblocker.post_contains_ad(message):
        for user in database.User.select() \
                .where(database.User.observing_channels.contains(str(message.sender_chat.id))):
            try:
                channel_info = await parserCore.get_chat_info_by_link(float(message.sender_chat.id))
                if message.text is not None:
                    text = f'Переслано из "{channel_info.title}"📢\n\n {message.text}'
                    await botCore.send_message(chat_id=user.user_id, text=text,
                                               reply_markup=rating.generate_rate_keyboard(
                                                   f"{message.sender_chat.id}_{message.message_id}"),
                                               disable_notifications=user.silent_mode)
                elif message.sticker is not None:
                    await botCore.send_message(user.user_id, f'Переслано из "{channel_info.title}"📢'
                                                             f"\n\nПросмотров:{message.views}",
                                               disable_notifications=user.silent_mode,
                                               reply_markup=None)
                    await botCore.bot.send_sticker(user.user_id, message.sticker.file_id,
                                               reply_markup=rating.generate_rate_keyboard(
                                                   f"{message.sender_chat.id}_{message.message_id}"))
                elif message.media:
                    text = f'Переслано (медиаконтент) из "{channel_info.title}"📢' \
                           f'\n\n {message.caption}\n\nПоддержка медиаконтента будет добавлена в ближайшее время'
                    await botCore.send_message(chat_id=user.user_id, text=text,
                                               reply_markup=rating.generate_rate_keyboard(
                                                   f"{message.sender_chat.id}_{message.message_id}"),
                                               disable_notifications=user.silent_mode)
            except utils.exceptions.BotBlocked as e:
                print(f"User {user.user_id} was deleted. Cause: {e.text}")
                database.User.delete().where(database.User.user_id == user.user_id).execute()
