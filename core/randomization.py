import string
from django.utils.crypto import get_random_string


def generate_slug():
    length = 40
    return get_random_string(length=length, allowed_chars=string.digits)
