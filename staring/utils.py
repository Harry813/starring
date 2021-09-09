from .customerSettings import Languages
from .text import *


def get_language_codes():
    langs = []
    for lang in Languages:
        langs.append((lang["CODE"], lang["NAME"]))
    return tuple(langs)


def get_basic_info():
    param = {
        "brandname": brand_name
    }
    return param
