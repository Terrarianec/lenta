from aiogram.dispatcher.filters import Command

from lenta_handlers import callback

from aiogram import Bot, Dispatcher, executor
from aiogram.types import CallbackQuery

from modules import database, channel, menus, admin

bot = Bot("1916928587:AAGXzNiY4Et1NPbA0q5Bi6Amtxowa4RY-4I")
dispatcher = Dispatcher(bot)


async def show_popup(call_id, text, show_alert=False):
    await dispatcher.bot.answer_callback_query(call_id, text, show_alert=show_alert)


async def edit_message_reply_markup(chat_id, message_id, reply_markup=None):
    await bot.edit_message_reply_markup(chat_id, message_id, reply_markup=reply_markup)


async def delete_message(chat_id, message_id):
    await dispatcher.bot.delete_message(chat_id,
                                        message_id)


async def forward_message(chat_id, from_chat_id, message_id):
    await dispatcher.bot.forward_message(chat_id,
                                         from_chat_id,
                                         message_id)


async def send_message(chat_id, text, reply_markup, disable_notifications=False):
    await dispatcher.bot.send_message(chat_id,
                                      text,
                                      reply_markup=reply_markup,
                                      disable_notification=disable_notifications)


'''
async def check_pro_expire():
    while True:
        users = User.select().where(User.is_pro == 1)
        for user in users:
            print(f"{user.pro_expires} < --- > {datetime.datetime.today()} ")
            if user.pro_expires <= datetime.datetime.today():
                await send_message_test(user.user_id, "Ваш PRO-статус истёк\n/pro - купить новый")
                print("Wiping user's " + str(user.user_id) + "PRO status")
                User.update(is_pro=False).where(User.user_id == user.user_id).execute()
        if len(users) > 0:
            print(f"PRO-status expired on {len(users)}! They should buy a new one!")
        await asyncio.sleep(1)
'''

@dispatcher.message_handler(Command('start'))
async def start(message):
    await send_message(message.from_user.id, 'Добро пожаловать!\n'
                                                     '/help - основные команды\n'
                                                     '/profile - Ваш профиль\n',reply_markup=None)


@dispatcher.message_handler(Command('help'))
async def commands_list(message):
    await send_message(message.from_user.id, "Комнады:\n"
                                             "/add (имя или URL канала) - добавить канал\n"
                                             "/remove - открыть меню удаления каналов\n"
                                             "/profile - Ваш профиль", reply_markup=None)


@dispatcher.message_handler(Command('add'))
async def add_channel(message):
    await send_message(message.from_user.id, await channel.add(message), reply_markup=None)


@dispatcher.message_handler(Command('remove'))
async def remove_channel(message):
    result = await menus.remove(message)
    await send_message(message.from_user.id, result[1], reply_markup=result[0])


@dispatcher.message_handler(Command('profile'))
async def profile(message):
    await menus.profile(message)


@dispatcher.message_handler(Command('pro'))
async def be_pro(message):
    result = menus.pro(message)
    await bot.send_message(message.from_user.id, result[1], reply_markup=result[0])


@dispatcher.message_handler(Command('br'))
async def broadcast(message):
    await admin.broadcast(message)


@dispatcher.message_handler(Command('user'))
async def get_user_by_id(message):
    await send_message(message.from_user.id, await admin.get_user(message), reply_markup=None)


@dispatcher.message_handler(Command('channel'))
async def get_channel_by_id(message):
    await send_message(message.from_user.id, await admin.get_user(message), reply_markup=None)


@dispatcher.message_handler(Command('banword'))
async def banword(message):
    await send_message(message.from_user.id, admin.banwords(message), reply_markup=None)


@dispatcher.callback_query_handler()
async def callback_handler(call: CallbackQuery):
    await callback.handle_callback(call)


@dispatcher.message_handler(content_types=["video"])
async def get_vid_data(message):
    await dispatcher.bot.send_message(message.from_user.id, 'Об этом видео: ' + message.video)


if __name__ == '__main__':
    database.init_database()
    executor.start_polling(dispatcher)
