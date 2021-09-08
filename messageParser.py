from telethon import TelegramClient, events
from peewee import *

# Remember to use your own values from my.telegram.org!
from telethon.tl.functions.channels import JoinChannelRequest

api_id = 7328736
api_hash = 'd2794f2700d1dc0141e9f0d3f84d5837'
client = TelegramClient('LNPS', api_id, api_hash)

db = SqliteDatabase('people.db')

observingChats = []

banwords = [""," "]

class User(Model):
    user_id = IntegerField()
    observingChannels = TextField()

    class Meta:
        database = db  # This model uses the "people.db" database.


async def main():
    # Getting information about yourself
    me = await client.get_entity("RustyTheCodeguy")

    # "me" is a user object. You can pretty-print
    # any Telegram object with the "stringify" method:
    print(me.stringify())

    # When you print something, you see a representation of it.
    # You can access all attributes of Telegram objects with
    # the dot operator. For example, to get the username:
    username = me.username

    # You can print all the dialogs/conversations that you are part of:

    # You can send messages to yourself...
    await client.send_message('RustyTheCodeguy', 'Hello, myself!')
    # ...to some chat ID
    # await client.send_message(-100123456, 'Hello, group!')
    # ...to your contacts
    # await client.send_message('+34600123123', 'Hello, friend!')
    # ...or even to any username
    # await client.send_message('username', 'Testing Telethon!')

    # You can, of course, use markdown in your messages:
    message = await client.send_message(
        'RustyTheCodeguy',
        'This call has **bold**, `code`, __italics__ and '
        'a [nice website](https://example.com)!',
        link_preview=False
    )

    # You can reply to messages directly if you have a call object
    # await call.reply('Cool!')
    # client(JoinChannelRequest("_Lpl4W_TVs4OGE6"))

    # Or send files, songs, documents, albums...
    # await client.send_file('me', '/home/me/Pictures/holidays.jpg')


@client.on(events.NewMessage(observingChats))
async def on_observing_chat_message_received(event):
    print("Recived call from observing chat")
    print(event.message.to_dict()['call'])


@client.on(events.NewMessage())
async def on_user_chat_message_received(event):
    if "/start" in event.text.lower():
        await client.send_message(event.message.chat_id, 'Добро пожаловать!\n'
                                                         '/help - основные команды\n'
                                                         '/profile - Ваш профиль\n'
                                                         '/lnews - новости разработки')
    if "/add" in event.text.lower():
        me = await client.get_entity("t.me/lentabot_news")

        print(me.id)
        inputString = event.text[5::]
        if " " in inputString or inputString == "":
            await client.send_message(event.message.chat_id, 'Синтаксис: /add (ссылка на канал)')
        else:
            try:
                channelInfo = await client.get_entity(inputString)
                channelsObserving = get_observing_channels(event)

                if channelInfo.id in channelsObserving:
                    await client.send_message(event.message.chat_id, 'За этим каналом вы уже следите.\n'
                                                                 'Удалить канал: /remove')
                else:
                    channelsObserving.append(''.join(str(channelInfo.id).split()))
                    User.update(
                        observingChannels=''.join([channel + " " for channel in cleanup_array(channelsObserving)])) \
                        .where(User.user_id == event.message.chat_id).execute()

                    await client.send_message(event.message.chat_id, f'Канал {channelInfo.title} '
                                                                 'добавлен в список отслеживаемых.\n'
                                                                 'Список всех каналов: /profile')
            except ValueError as ve:
                print(ve)
                await client.send_message(event.message.chat_id, f'Пожалуйста, введите корректную ссылку на канал,'
                                                                 f' пример: "/add t.me/lentabot_news"')
    if "/remove" in event.text.lower():
        if " " in event.text[8::] or event.text[8::] == "":
            await client.send_message(event.message.chat_id, 'Синтаксис: /remove (ID)')
        else:
            channelsObserving = get_observing_channels(event)

            if not event.text[8::] in channelsObserving:
                await client.send_message(event.message.chat_id, 'Этот канал нельзя удалить: вы за ним не следите.\n'
                                                                 'Добавить канал: /add')
            else:
                channelsObserving.remove(''.join(event.text[8::].split()))
                User.update(
                    observingChannels=''.join([channel + " " for channel in cleanup_array(channelsObserving)])) \
                    .where(User.user_id == event.message.chat_id).execute()

                await client.send_message(event.message.chat_id, f'Канал {event.text[8::]} '
                                                                 'был удалён из списка отслеживаемых.\n'
                                                                 'Список всех каналов: /profile')

    if "/profile" in event.text.lower():
        a = await client.send_message(event.message.chat_id, 'Ваш профиль')

        await a.reply('Ваши подписки: \n' + ''.join([channel + "\n" for channel in get_observing_channels(event)]))


def check_user_exsistance(eventData):
    user = User.select().where(User.user_id == eventData.sender_id)
    if not user.exists():
        query = User.insert(user_id=eventData.sender_id, observingChannels="-1001511257641")
        query.execute()
        user = User.select().where(User.user_id == eventData.sender_id)
    return user


def get_observing_channels(event):
    userObject = check_user_exsistance(event)

    channelsObserving = []
    for i in userObject:
        channelsObserving = i.observingChannels.split(" ")

    return channelsObserving

def cleanup_array(dirtyArray):
    for banword in banwords:
        if banword in dirtyArray:
            dirtyArray.remove(banword)
    return dirtyArray

with client:
    db.connect()
    db.create_tables([User])
    client.run_until_disconnected()
