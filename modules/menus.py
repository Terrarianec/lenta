from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import botCore
import parserCore
from modules import misc, database


async def remove(call):
    remove_kb = InlineKeyboardMarkup(resize_keyboard=True)

    for channel in database.get_observing_channels(call):
        if channel == "" or " " in channel:
            pass
        else:
            channel_info = await parserCore.get_chat_info_by_link(float(channel))
            remove_kb.add(InlineKeyboardButton(f"{channel_info.title}", callback_data=channel_info.id))

    remove_kb.add(InlineKeyboardButton(f"Закрыть", callback_data="cancel"))

    return remove_kb, 'Выбери канал для удаления'


async def profile(call):
    profile_kb = InlineKeyboardMarkup(resize_keyboard=True)
    profile_kb.add(InlineKeyboardButton(f'Переключить "тихий режим"', callback_data="profile_silent_mode"))
    profile_kb.add(InlineKeyboardButton(f'Сброс профиля', callback_data="profile_wipe_data"))

    profile_header = await botCore.bot.send_message(call.from_user.id,
                                                    'Ваш профиль\n\n'
                                                    '(данные по подпискам появятся через несколько секунд)',
                                                    reply_markup=profile_kb)
    result = ""
    channels = database.get_observing_channels(call)
    for channel in channels:
        if channel == "" or " " in channel:
            pass
        else:
            channel_info = await parserCore.get_chat_info_by_link(float(channel))
            result += f"{misc.generate_random_color()}" \
                      f"{channel_info.title}" \
                      f" <--> " \
                      f"{channel_info.members_count} " \
                      f"участников\n"
    user = database.check_user_exsistance(call).get()
    if user.is_pro:
        sub_limit = 30
    else:
        sub_limit = 7
    await profile_header.reply(f'Ваши подписки ({str(len(channels))}/{sub_limit}): \n' + result)


def pro(call):
    user = database.check_user_exsistance(call).get()
    if user.is_pro:
        return None, f'Ты уже на одной волне с нами!\nТвой PRO-статус истекает {user.pro_expires}'
    else:
        profile_kb = InlineKeyboardMarkup(resize_keyboard=True)
        profile_kb.add(InlineKeyboardButton(f'Стать PRO 😎', url="t.me/r2c_paymentBot"))

        return profile_kb, 'Не будь нублом, приобретай PRO\n' \
                           'C PRO-подпиской у тебя появляются такие возможности, как\n' \
                           '✅ Добавлять до 30 чатов в отслеживаемые\n' \
                           '✅ Отслеживать не только каналы, но и группы\n' \
                           '✅ Получить доступ к плюшкам первым'
