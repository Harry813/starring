from django import template
from django.urls import translate_url

from staring.customerSettings import Languages

register = template.Library()


@register.simple_tag
def get_flag_by_code(code):
    for lang in Languages:
        if lang["CODE"] == code:
            return lang["FLAG"]
    return "IMG/FLAGS/UNKNOWN.png"


@register.simple_tag(takes_context=True)
def change_lang(context, lang=None, *args, **kwargs):
    path = context['request'].path
    return translate_url('path', lang)
