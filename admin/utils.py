from staring.customerSettings import ADMMegaMenu, Slot_end, Slot_start, Slot_interval, Slot_duration
from datetime import datetime, date, time, timedelta

from staring.models import NavigatorSector, NavigatorItem, IndexListItem

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


def reorder(c, q=None, item=None, index=-1):
    if not hasattr(c, "order"):
        raise AttributeError(f"class {c} do not have attribute \"order\"")

    if q:
        items = c.objects.filter(q).order_by('order')
    else:
        items = c.objects.all().order_by('order')

    items = list(items)

    if item:
        if index < 0:
            items.append(item)
        else:
            try:
                items.pop(items.index(item))
            except ValueError:
                pass
            finally:
                items.insert(index, item)

    for i in range(len(items)):
        it = items[i]
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
