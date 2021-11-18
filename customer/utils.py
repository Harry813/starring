from staring.customerSettings import IndexListItems, NavItems
from staring.models import NewsSector, News


def get_customer_info():
    dic = {
        "indexList": IndexListItems,
        "navItems": NavItems,
    }
    return dic


def get_news():
    accr = []
    sectors = NewsSector.objects.all()
    for sector in sectors:
        dic = {
            "sector": sector,
            "news": News.objects.filter(sector=sector)[:sector.max_news]
        }
        accr.append(dic)
    return accr
