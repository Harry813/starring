from django import template

from staring.customerSettings import Languages

register = template.Library()


def get_flag_by_code(code):
    for lang in Languages:
        if lang["CODE"] == code:
            return lang["FLAG"]
    return "IMG/FLAGS/UNKNOWN.png"
