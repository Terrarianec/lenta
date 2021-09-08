import settings


def post_contains_ad(post):
    if post.chat.id not in settings.group_whitelist:
        if post.text is not None:
            if post.text.lower() not in settings.banlist:
                return True
        elif post.caption is not None:
            if post.caption.lower() not in settings.banlist:
                return True
        else:
            return False
    else:
        return True
