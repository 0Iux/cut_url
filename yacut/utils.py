from random import choice
import string

from .models import URLMap


def get_unique_short_id(length=6):
    characters = string.ascii_letters + string.digits
    while True:
        short_id = ''.join(choice(characters) for _ in range(length))
        if URLMap.query.filter_by(short=short_id).count() == 0:
            return short_id


def is_valid_short_id(short):
    if len(short) > 16:
        return False
    valid_symbols = string.ascii_letters + string.digits
    for letter in short:
        if letter not in valid_symbols:
            return False
    return True
