import botCore
import parserCore
from modules import database, misc


async def remove(call):
    channels_observing = database.get_observing_channels(call)
    if call.data not in channels_observing:
        return 'Этот канал нельзя удалить: вы за ним не следите.\n' \
               'Добавить канал: /add'
    else:
        channels_observing.remove(''.join(call.data.split()))
        database.User.update(
            observing_channels=''.join([channel + " " for channel in misc.cleanup_array(channels_observing)])) \
            .where(database.User.user_id == call.from_user.id).execute()
        channel_info = await parserCore.get_chat_info_by_link(float(call.data))
        return f'Канал {channel_info.title} ' \
               f'был удалён из списка отслеживаемых.' \
               f'\nСписок всех каналов: /profile'


async def add(call):
    input_string = call.text[5::]
    if " " in input_string or input_string == "":
        return 'Синтаксис: /add (ссылка на канал)'
    else:
        #try:
            if "t.me/" in call.text:
                input_string = call.text[10::]

            if "http://" in call.text:
                input_string = call.text[17::]

            if "https://" in call.text:
                input_string = call.text[18::]

            channel_info = await parserCore.get_chat_info_by_link(input_string)
            channels_observing = database.get_observing_channels(call)
            is_can_add_more = database.can_user_add_more_channels(channels_observing, call)
            if is_can_add_more[0]:
                if str(channel_info.id) in channels_observing:
                    return 'За этим каналом вы уже следите.\n' \
                           'Удалить канал: /remove'

                else:
                    await parserCore.join_chat(channel_info.id)
                    channels_observing.append(''.join(str(channel_info.id).split()))
                    database.User.update(
                        observing_channels=''.join([chnl + " " for chnl in misc.cleanup_array(channels_observing)])) \
                        .where(database.User.user_id == call.from_user.id).execute()

                    return f'Канал {channel_info.title} ' \
                           'добавлен в список отслеживаемых.\n' \
                           'Список всех каналов: /profile'
            else:
                return is_can_add_more[1]

        #except Exception as _:  # Check, what kind of Exception generates wrong URL
            #return 'Пожалуйста, введите корректную ссылку на канал,' \
                   #f' пример: "/add t.me/lentabot_news"'
