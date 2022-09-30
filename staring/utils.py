import os
import random
import shutil
from datetime import datetime
from decimal import Decimal

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.translation import gettext as _

from . import settings
from .customerSettings import Languages
from .text import *


def get_language_codes ():
    langs = []
    for lang in Languages:
        langs.append((lang["CODE"], lang["NAME"]))
    return tuple(langs)


def get_basic_info ():
    param = {
        "brandname": brand_name
    }
    return param


def get_upload_directory ():
    date_path = datetime.now().strftime("%Y/%m/%d")

    # Complete upload path (upload_path + date_path).
    upload_path = os.path.join(settings.CKEDITOR_UPLOAD_PATH, date_path)
    return os.path.join(settings.MEDIA_ROOT, upload_path)


def get_media_url (file_name):
    args = [settings.CKEDITOR_UPLOAD_PATH, datetime.now().strftime("%Y/%m/%d"), file_name]
    return settings.MEDIA_URL + "/".join(arg.strip("/") for arg in args)


def remove_upload_directory ():
    # Called on test setup
    # Avoid falling in the use case chere django append a hash to the file name
    # to prevent file collisions
    shutil.rmtree(get_upload_directory(), ignore_errors=True)


def get_absolute_media_path (file_name):
    upload_directory = get_upload_directory()
    return os.path.join(upload_directory, file_name)


def get_absolute_name (class_or_function):
    return "%s.%s" % (class_or_function.__module__, class_or_function.__name__)


def get_subject_CLB (test, subject, score):
    """
    Get the CLB of a subject test.
    :param test: the test code
    :type test: int
    :param subject: the subject code, "L" for listening, "S" for speaking, "R" for reading, "W" for writing
    :type subject: str
    :param score: the score
    :type score: Decimal
    :return: the CLB
    :rtype: int
    """
    if test == 0:
        if score >= 10:
            return 10
        elif 4 <= score <= 9:
            return score
        else:
            return 3
    elif test == 1:
        if subject == "L":
            if score >= 8.5:
                return 10
            elif score >= 8.0:
                return 9
            elif score >= 7.5:
                return 8
            elif score >= 6.0:
                return 7
            elif score >= 5.5:
                return 6
            elif score >= 5.0:
                return 5
            elif score >= 4.5:
                return 4
            else:
                return 3
        elif subject == "S":
            if score >= 7.5:
                return 10
            elif score >= 7.0:
                return 9
            elif score >= 6.5:
                return 8
            elif score >= 6.0:
                return 7
            elif score >= 5.5:
                return 6
            elif score >= 5.0:
                return 5
            elif score >= 4.0:
                return 4
            else:
                return 3
        elif subject == "R":
            if score >= 8:
                return 10
            elif score >= 7:
                return 9
            elif score >= 6.5:
                return 8
            elif score >= 6:
                return 7
            elif score >= 5:
                return 6
            elif score >= 4:
                return 5
            elif score >= 3.5:
                return 4
            else:
                return 3
        elif subject == "W":
            if score >= 7.5:
                return 10
            elif score >= 7.0:
                return 9
            elif score >= 6.5:
                return 8
            elif score >= 6.0:
                return 7
            elif score >= 5.5:
                return 6
            elif score >= 5.0:
                return 5
            elif score >= 4.0:
                return 4
            else:
                return 3
    elif test == 2:
        if subject == "L":
            if score >= 316:
                return 10
            elif 298 <= score <= 315:
                return 9
            elif 280 <= score <= 297:
                return 8
            elif 249 <= score <= 279:
                return 7
            elif 217 <= score <= 248:
                return 6
            elif 181 <= score <= 216:
                return 5
            elif 149 <= score <= 180:
                return 4
            else:
                return 3
        elif subject == "S":
            if score >= 393:
                return 10
            elif 371 <= score <= 392:
                return 9
            elif 349 <= score <= 370:
                return 8
            elif 310 <= score <= 348:
                return 7
            elif 271 <= score <= 309:
                return 6
            elif 226 <= score <= 270:
                return 5
            elif 181 <= score <= 225:
                return 4
            else:
                return 3
        elif subject == "R":
            if score >= 263:
                return 10
            elif 248 <= score <= 262:
                return 9
            elif 233 <= score <= 247:
                return 8
            elif 207 <= score <= 232:
                return 7
            elif 181 <= score <= 206:
                return 6
            elif 151 <= score <= 180:
                return 5
            elif 121 <= score <= 150:
                return 4
            else:
                return 3
        elif subject == "W":
            if score >= 393:
                return 10
            elif 371 <= score <= 392:
                return 9
            elif 349 <= score <= 370:
                return 8
            elif 310 <= score <= 348:
                return 7
            elif 271 <= score <= 309:
                return 6
            elif 226 <= score <= 270:
                return 5
            elif 181 <= score <= 225:
                return 4
            else:
                return 3
    elif test == 3:
        if subject == "L":
            if score >= 549:
                return 10
            elif score >= 523:
                return 9
            elif score >= 503:
                return 8
            elif score >= 458:
                return 7
            elif score >= 398:
                return 6
            elif score >= 369:
                return 5
            elif score >= 331:
                return 4
            else:
                return 3
        elif subject in ["S", "W"]:
            if score >= 16:
                return 10
            elif score >= 14:
                return 9
            elif score >= 12:
                return 8
            elif score >= 10:
                return 7
            elif score >= 7:
                return 6
            elif score >= 6:
                return 5
            elif score >= 4:
                return 4
            else:
                return 3
        elif subject == "R":
            if score >= 549:
                return 10
            elif score >= 524:
                return 9
            elif score >= 499:
                return 8
            elif score >= 453:
                return 7
            elif score >= 406:
                return 6
            elif score >= 375:
                return 5
            elif score >= 342:
                return 4
            else:
                return 3


def get_first_language_score (marriage_class, clb):
    if marriage_class == 0:
        if clb <= 3:
            return 0
        elif clb == 4 or clb == 5:
            return 6
        elif clb == 6:
            return 9
        elif clb == 7:
            return 17
        elif clb == 8:
            return 23
        elif clb == 9:
            return 31
        elif clb >= 10:
            return 34
    elif marriage_class == 1:
        if clb <= 3:
            return 0
        elif clb == 4 or clb == 5:
            return 6
        elif clb == 6:
            return 8
        elif clb == 7:
            return 16
        elif clb == 8:
            return 22
        elif clb == 9:
            return 29
        elif clb >= 10:
            return 32
    else:
        return 0


def get_second_language_score (clb=0):
    if clb == 5 or clb == 6:
        return 1
    elif clb == 7 or clb == 8:
        return 3
    elif clb >= 9:
        return 6
    else:
        return 0


def get_partner_language_score (clb=0):
    if clb == 5 or clb == 6:
        return 1
    elif clb == 7 or clb == 8:
        return 3
    elif clb >= 9:
        return 5
    else:
        return 0


def generate_order_id ():
    s = "APPT" + datetime.now().strftime('%Y%m%d%H%M%S') + str(random.randint(0, 9999)).zfill(4)
    return s


def get_appt_price_total (appt, discount=None, coupon=None):
    """

    :param appt:
    :type appt: Appointment
    :param discount:
    :type discount:
    :param coupon:
    :type coupon:
    :return:
    :rtype:
    """
    price = appt.price
    return price


def send_email_with_template (subject, context, recipient_list, template="email_template/email_template.html",
                              fail_silently=False, auth_user=None, auth_password=None, connection=None):
    param = {
        "url_root": "star.ourcv.net",
        **context
    }
    html_email = render_to_string(template, param)
    plain_text = strip_tags(html_email)
    send_mail(
        subject=subject,
        message=plain_text,
        html_message=html_email,
        from_email="noreply@ourcv.net",
        recipient_list=recipient_list,
        fail_silently=fail_silently,
        auth_user=auth_user,
        auth_password=auth_password,
        connection=connection
    )
