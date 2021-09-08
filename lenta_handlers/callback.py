import botCore
import parserCore
import settings
from modules import database, rating, misc, channel


async def handle_callback(call):
    if call.data == "cancel":
        await call.message.delete()

    elif "profile_" in call.data:
        if "profile_silent_mode" == call.data:
            user_settings = database.check_user_exsistance(call).get()
            database.User.update(silent_mode=not user_settings.silent_mode) \
                .where(database.User.user_id == call.from_user.id).execute()
            await botCore.send_message(call.from_user.id,
                                       f'Уведомления будут приходить без звука: {not user_settings.silent_mode}',
                                       reply_markup=None)

        if "profile_wipe_data" == call.data:
            database.User.update(observing_channels="-1001511257641", silent_mode=False).where(
                database.User.user_id == call.from_user.id).execute()
            await botCore.send_message(call.from_user.id, f'Профиль очищен\nPRO-статус не сброшен')

    elif "report" in call.data:
        await botCore.send_message(settings.admin_id,
                                   f'Сообщение о нарушении от пользователя @{call["from"].username or call["from"].id}',
                                   reply_markup=None)
        await botCore.forward_message(settings.admin_id, call.from_user.id, call.message.message_id)
        await botCore.delete_message(call.from_user.id, call.message.message_id)
        await botCore.send_message(call.from_user.id, f'Сообщение было успешно отправлено на модерацию\n\n'
                                                      f'Спасибо!', reply_markup=None)

    elif "rateup_" in call.data:
        post = call.data[7::].split("_")
        post = misc.cleanup_array(post)
        await botCore.show_popup(call_id=call.id,
                                 text=await rating.send_post_rating(f"{post[0]}/{post[1]}",
                                                                    call.from_user.id,
                                                                    call.message, 1),
                                 show_alert=False)

    elif "ratedown_" in call.data:
        post = call.data[9::].split("_")
        post = misc.cleanup_array(post)
        await botCore.show_popup(call_id=call.id,
                                 text=await rating.send_post_rating(f"{post[0]}/{post[1]}",
                                                                    call.from_user.id,
                                                                    call.message, -1),
                                 show_alert=False)

    else:
        await botCore.send_message(call.from_user.id, await channel.remove(call), reply_markup=None)
