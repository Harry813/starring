from staring.customerSettings import IndexListItems, navi_item_per_col
from staring.models import NewsSector, News, NavigatorSector, NavigatorItem


def get_customer_info():
    dic = {
        "indexList": IndexListItems,
        "navigator": []
    }

    for sec in NavigatorSector.objects.all():
        itemslist = list(NavigatorItem.objects.filter(sector=sec))
        dic["navigator"].append({
            "sector": sec,
            "itemslist": [itemslist[i: i+navi_item_per_col] for i in range(0, len(itemslist), navi_item_per_col)]
        })
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
