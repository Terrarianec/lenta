from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import botCore
import news_cathegoriser
from modules import database, misc


def generate_rate_keyboard(callback_data):
    rate_kb = InlineKeyboardMarkup(resize_keyboard=True)

    rate_kb.add(InlineKeyboardButton("👍", callback_data=f"rateup_{callback_data}"),
                InlineKeyboardButton("📣", callback_data=f"report"),
                InlineKeyboardButton("👎", callback_data=f"ratedown_{callback_data}"))

    return rate_kb


async def send_post_rating(post_id, user_id, post_data, post_rating):
    post_content = news_cathegoriser.get_post_theme(await news_cathegoriser.cleanup_input(post_data.text))
    database.check_post_exsistance_in_db(post_id, post_content)
    posts = database.Post.select().where(database.Post.post_id == post_id)

    for post in posts:

        user_id = str(user_id)

        is_voted = False

        post_liked = post.post_user_likes.split(" ")
        post_disliked = post.post_user_dislikes.split(" ")

        if post_rating > 0:

            if user_id not in misc.cleanup_array(post_liked):
                if user_id in misc.cleanup_array(post_disliked):
                    post_disliked.remove(user_id)
                    post_rating += 1
                post_liked.append(user_id)
                post_rate = post.post_rating + post_rating
                is_voted = True
            else:
                post_liked.remove(user_id)
                post_rate = post.post_rating - post_rating

        else:
            if user_id not in misc.cleanup_array(post_disliked):
                if user_id in misc.cleanup_array(post_liked):
                    post_liked.remove(user_id)
                    post_rating -= 1
                post_disliked.append(user_id)
                post_rate = post.post_rating + post_rating
                is_voted = True
            else:
                post_disliked.remove(user_id)
                post_rate = post.post_rating - post_rating

        database.Post.update(post_rating=post_rate,
                             post_user_likes=''.join([p_l + " " for p_l in misc.cleanup_array(post_liked)]),
                             post_user_dislikes=''.join([p_dl + " " for p_dl in misc.cleanup_array(post_disliked)])) \
            .where(database.Post.post_id == post_id).execute()

        if is_voted:
            await botCore.edit_message_reply_markup(user_id, post_data.message_id)
            if post_rating > 0:
                return "Ваша оценка учтена 📈"
            else:
                return "Ваша оценка учтена 📉"
        else:
            return "Ваша оценка отменена 📊"
