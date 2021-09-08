import random
import string

import settings


def cleanup_array(array):
    bad_words = ["", " ", "  "]
    output = []
    for a_word in array:
        if a_word not in bad_words:
            output.append(a_word)
    return output


def generate_random_color():
    colors = ["🟥", "🟧", "🟨", "🟩", "🟦", "🟪"]
    return random.choice(colors)


def generate_random_key(lenght=10, seed=random.randint(11111, 99999)):
    random.Random().seed(str(seed))
    return ''.join([random.choice(string.ascii_letters) for _ in range(lenght)])


def is_admin(user_id):
    return user_id == settings.admin_id
