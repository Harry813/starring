from staring.customerSettings import navi_item_per_col
from staring.models import NewsSector, News, NavigatorSector, NavigatorItem, IndexListSector, IndexListItem, \
    IndexSidebarItem


def get_customer_info():
    dic = {
        "navigator": []
    }

    for sec in NavigatorSector.objects.all():
        itemslist = list(NavigatorItem.objects.filter(sector=sec))
        dic["navigator"].append({
            "sector": sec,
            "itemslist": [itemslist[i: i+navi_item_per_col] for i in range(0, len(itemslist), navi_item_per_col)]
        })

    dic["questions"] = list(IndexSidebarItem.objects.all())
    return dic


def get_news():
    li = []
    sectors = NewsSector.objects.all()
    for sector in sectors:
        dic = {
            "sector": sector,
            "news": News.objects.filter(sector=sector)[:sector.max_news]
        }
        li.append(dic)
    return li


def get_index_list():
    li = []
    sectors = IndexListSector.objects.all()
    for sec in sectors:
        dic = {
            "sector": sec,
            "items": IndexListItem.objects.filter(sector=sec)
        }
        li.append(dic)
    return li
