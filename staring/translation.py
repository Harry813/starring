from modeltranslation.translator import register, TranslationOptions
from .models import Article, NavigatorSector, NavigatorItem, IndexListSector, IndexListItem


@register(Article)
class ArticleTranslation(TranslationOptions):
    fields = ("title", "author", "description", "keywords", "content")


@register(NavigatorSector)
class NavigatorSectorTranslation(TranslationOptions):
    fields = ("name", )


@register(NavigatorItem)
class NavigatorItemTranslation(TranslationOptions):
    fields = ("name", )


@register(IndexListSector)
class IndexListSectorTranslation(TranslationOptions):
    fields = ("name", )


@register(IndexListItem)
class IndexListItemTranslation(TranslationOptions):
    fields = ("name", )
