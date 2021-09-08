import asyncio
from modules import messages
from pyrogram import Client, filters

api_id = 7328736
api_hash = 'd2794f2700d1dc0141e9f0d3f84d5837'
client = Client('LentaParsingService', api_id, api_hash)
client.start()

globalTickTime = 30  # seconds
joinAfter = 0.5  # Joins next new channel every amount of time


def get_chat_info_by_link(url):
    a = client.get_chat(url)
    return a


async def join_channels_from_global_channel_list(chats):
    async for chat in chats:
        client.join_chat(chat)
        await asyncio.sleep(joinAfter)


@client.on_message(filters.channel & ~filters.edited)
async def get_new_message(client, message):
    await messages.send_post(message)


async def read_messages(chat_id):
    return await client.get_messages(chat_id=chat_id)


async def join_chat(chat_id):
    try:
        await client.join_chat(chat_id)
    except Exception as e:
        print(e)
