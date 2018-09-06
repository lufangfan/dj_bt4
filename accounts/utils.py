import os
import uuid


def get_avatar_path(instance, filename):
    avatar = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), avatar)
    return os.path.join('avatar', filename)