from modeltranslation.translator import register, TranslationOptions
from .models import Article, NavigatorSector, NavigatorItem


@register(Article)
class ArticleTranslation(TranslationOptions):
    fields = ("title", "author", "description", "keywords", "content")


@register(NavigatorSector)
class NavigatorSectorTranslation(TranslationOptions):
    fields = ("name", )


@register(NavigatorItem)
class NavigatorItemTranslation(TranslationOptions):
    fields = ("name", )

