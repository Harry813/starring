from .customerSettings import Languages


def get_language_codes():
    langs = []
    for lang in Languages:
        langs.append((lang["CODE"], lang["NAME"]))
    return tuple(langs)
