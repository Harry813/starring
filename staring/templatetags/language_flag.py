from django import template
from django.urls import translate_url, resolve, reverse
from django.utils.translation import get_language, activate

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
    """
    Get active page's url by a specified language
    Usage: {% change_lang 'en' %}
    """

    path = context['request'].path
    url_parts = resolve(path)

    url = path
    cur_language = get_language()
    try:
        activate(lang)
        url = reverse(url_parts.view_name, kwargs=url_parts.kwargs)
    finally:
        activate(cur_language)
    return "%s" % url
