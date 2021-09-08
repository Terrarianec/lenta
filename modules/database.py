from peewee import *

db = SqliteDatabase('people.db')


class User(Model):
    user_id = IntegerField()
    observing_channels = TextField()
    silent_mode = BooleanField()
    is_pro = BooleanField()
    pro_expires = TimestampField()

    class Meta:
        database = db  # This model uses the "people.db" database.


class Post(Model):
    post_id = IntegerField()
    post_rating = IntegerField()
    post_content = TextField()
    post_user_likes = TextField()
    post_user_dislikes = TextField()

    class Meta:
        database = db  # This model uses the "people.db" database.


def init_database():
    db.connect()
    db.create_tables([User, Post])


def check_user_exsistance(event_data):
    user = User.select().where(User.user_id == event_data.from_user.id)
    if not user.exists():
        query = User.insert(user_id=event_data.from_user.id, observing_channels="-1001511257641", silent_mode=False,
                            is_pro=False, pro_expires=0)
        query.execute()
        user = User.select().where(User.user_id == event_data.from_user.id)
    return user


def get_observing_channels(event):
    user_object = check_user_exsistance(event)

    channels_observing = []
    for i in user_object:
        channels_observing = i.observing_channels.split(" ")

    return channels_observing


def check_post_exsistance_in_db(post_id, post_data):
    posts = Post.select().where(Post.post_id == post_id)
    if not posts.exists():
        Post.insert(post_id=post_id,
                    post_rating=0,
                    post_content=post_data,
                    post_user_likes=" ",
                    post_user_dislikes=" ").execute()


def can_user_add_more_channels(channels, call):
    if len(channels) >= 7 and not \
            User.select(User.is_pro).where(User.user_id == call.from_user.id).get():
        return False, 'Ты не можешь добавить больше 7 каналов\nХочешь больше? /pro'
    elif len(channels) >= 30:
        return False, 'Ты не можешь добавить больше 30 каналов'
    else:
        return True, None
