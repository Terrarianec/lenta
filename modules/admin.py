import botCore
import parserCore
import settings
from modules import misc, database
from aiogram import utils


async def broadcast(call):
    if misc.is_admin(call.chat.id):
        for user in database.User.select():
            try:
                text = f"Оповещение:\n{call.text[4::]}"
                await botCore.send_message(chat_id=user.user_id, text=text,
                                           disable_notifications=user.silent_mode, reply_markup=None)
            except utils.exceptions.BotBlocked as e:
                print(f"User {user.user_id} was deleted. Cause: {e.text}")
                database.User.delete().where(database.User.user_id == user.user_id).execute()


async def get_user(call):
    if misc.is_admin(call["from"].id):
        if not call.text[6::] == "":
            user = database.User.select().where(database.User.user_id == call.text[6::]).get()
            try:
                chat_data = await botCore.bot.get_chat(chat_id=user.user_id)
                text = f"Информация о пользователе:\n" \
                       f"ID: {chat_data.id}; Имя пользователя: {chat_data.username}\n" \
                       f"Имя: {chat_data.first_name}; Фамилия: {chat_data.last_name}\n\n" \
                       f"Информация внутри бота: \n" \
                       f"Подписан на каналы: {user.observing_channels}\n" \
                       f"Тихий режим включён: {user.silent_mode}\n\n" \
                       f"Для получения информации о каналах, пиши /channel"
                return text
            except utils.exceptions.BotBlocked as e:
                print(f"User {user.user_id} was deleted. Cause: {e.text}")
                database.User.delete().where(database.User.user_id == user.user_id).execute()
        else:
            users = database.User.select(database.User.user_id)
            userlist = ""
            for user in users:
                userlist += str(user.user_id) + "\n"
            return f"Список ползователей бота:\n{userlist}"
    else:
        return "🧐 Это команда не для пользователей"


async def get_channel(call):
    if misc.is_admin(call["from"].id):
        chat_data = await parserCore.client.get_chat(chat_id=call.text[9::])
        text = f"Информация о канале:\n" \
               f"ID: {chat_data.id}; Имя канала: {chat_data.username}\n" \
               f"Заголовок: {chat_data.title}\n\n"

        if chat_data.pinned_message is not None:
            text += f"Закреплённое сообщение: {chat_data.pinned_message.text or chat_data.pinned_message.caption}\n" \
                    f"Закреплено: {str(chat_data.pinned_message.date)}"

        return text
    else:
        return "🧐 Это команда не для пользователей"


def banwords(call):
    if misc.is_admin(call.from_user.id):
        text = call.text[9::]
        if text == "":
            return f"Список запрещённх слов: {settings.banlist}"
        elif "remove_word" in text:
            text = call.text[21::]
            return f"Слово {text} было удалено из списка!"
            settings.banlist.remove(text)
        else:
            return f"Слово {text} было добавлено в список!"
            settings.banlist.append(text)
