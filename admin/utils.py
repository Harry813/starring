from staring.customerSettings import ADMMegaMenu, Slot_end, Slot_start, Slot_interval, Slot_duration
from datetime import datetime, date, time, timedelta

from staring.models import NavigatorSector, NavigatorItem

TIMESLOT_TIME_FORMAT = '%I:%M %p'
TIMESLOT_INTERVAL = timedelta(minutes=+Slot_interval)
TIMESLOT_START_TIME = time(Slot_start)
TIMESLOT_END_TIME = time(Slot_end)
TIMESLOT_DURATION = timedelta(minutes=+45)


def get_admin_info():
    param = {
        "mega_menu": ADMMegaMenu
    }
    return param


def navigator_item_reorder(sector_id, item=None):
    """

    :param sector_id:
    :type sector_id: int
    :param item:
    :type item: NavigatorItem
    """
    if item:
        navi_items = NavigatorSector.objects.filter(sector_id=sector_id)
        navi_items.insert(item.order, item)
    else:
        navi_items = NavigatorSector.objects.filter(sector_id=sector_id)

    for i in range(len(navi_items)):
        it = navi_items[i]
        it.order = i
        it.save()


# diff
def time_delta_total_seconds(time_delta):
    """
    Calculate the total number of seconds represented by a
    ``datetime.timedelta`` object
    """
    return time_delta.days * 3600 + time_delta.seconds


def timeslot_24_options(
        interval=TIMESLOT_INTERVAL,
        start_time=TIMESLOT_START_TIME,
        end_time=TIMESLOT_END_TIME,
        fmt=TIMESLOT_TIME_FORMAT
):
    """
    Create a list of time slot options in the format of 2-tuples containing a 24-hour time value and a 12-hour temporal
    representation
    """
    dt = datetime.combine(date.today(), time(0))
    dtstart = datetime.combine(dt.date(), start_time)
    dtend = datetime.combine(dt.date(), end_time)
    options = []

    while dtstart <= dtend:
        options.append((str(dtstart.time()), dtstart.strftime(fmt)))
        dtstart += interval

    return options


def timeslot_12_options(
        interval=TIMESLOT_INTERVAL,
        start_time=TIMESLOT_START_TIME,
        end_time=TIMESLOT_END_TIME,
        fmt=TIMESLOT_TIME_FORMAT
):
    """
    Create a list of time slot options in the format of 2-tuples containing a 12-hour time value and a 12-hour temporal
    representation
    """
    dt = datetime.combine(date.today(), time(0))
    dtstart = datetime.combine(dt.date(), start_time)
    dtend = datetime.combine(dt.date(), end_time)
    options = []

    delta = time_delta_total_seconds(dtstart - dt)
    seconds = time_delta_total_seconds(interval)
    while dtstart <= dtend:
        options.append((delta, dtstart.strftime(fmt)))
        dtstart += interval
        delta += seconds

    return options


default_timeslot_options = timeslot_24_options()
default_timeslot_offset_options = timeslot_12_options()
