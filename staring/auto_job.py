from datetime import timedelta

from .models import *


def clean_evaluations():
    """
    Clean evaluations table.
    """
    clear_crs()


def clear_crs():
        crs = CRS.objects.filter(customer__isnull=True)
        msg = f"[DELETE]@{timezone.now()} {crs.count()} CRS evaluations deleted.\n"
        for c in crs:
            if timezone.now() - c.created_at > timedelta(days=7):
                msg += f"  - {str(crs)}\n"
                c.delete()
        return msg


def release_meeting_slot():
    """
    Release meeting slot.
    """
    count = 0
    meeting_slots = MeetingSlot.objects.filter(status="LOCKED", start_datetime__gt=timezone.now())
    msg = ""
    for meeting_slot in meeting_slots:
        appointments = Appointment.objects.filter(slot=meeting_slot,
                                                  updated_at__gte=timezone.now() - timedelta(minutes=30))
        if appointments:
            for appointment in appointments:
                count += 1
                appointment.status = "UNPAID"
                msg = f"  - {appointment} status change to \"UNPAID\".\n"
                appointment.save()
                meeting_slot.status = "AVAILABLE"
                meeting_slot.save()
                msg += f"    {meeting_slot} released.\n\n"
        else:
            meeting_slot.status = "AVAILABLE"
            meeting_slot.save()
            msg += f"  - {meeting_slot} released.\n\n"

    return f"[RELEASE]@{timezone.now()} {count} meeting slots released.\n" + msg
