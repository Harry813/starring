import os
import shutil
from datetime import datetime

from . import settings
from .customerSettings import Languages
from .text import *


def get_language_codes():
    langs = []
    for lang in Languages:
        langs.append((lang["CODE"], lang["NAME"]))
    return tuple(langs)


def get_basic_info():
    param = {
        "brandname": brand_name
    }
    return param


def get_upload_directory():
    date_path = datetime.now().strftime("%Y/%m/%d")

    # Complete upload path (upload_path + date_path).
    upload_path = os.path.join(settings.CKEDITOR_UPLOAD_PATH, date_path)
    return os.path.join(settings.MEDIA_ROOT, upload_path)


def get_media_url(file_name):
    args = [settings.CKEDITOR_UPLOAD_PATH, datetime.now().strftime("%Y/%m/%d"), file_name]
    return settings.MEDIA_URL + "/".join(arg.strip("/") for arg in args)


def remove_upload_directory():
    # Called on test setup
    # Avoid falling in the use case chere django append a hash to the file name
    # to prevent file collisions
    shutil.rmtree(get_upload_directory(), ignore_errors=True)


def get_absolute_media_path(file_name):
    upload_directory = get_upload_directory()
    return os.path.join(upload_directory, file_name)


def get_absolute_name(class_or_function):
    return "%s.%s" % (class_or_function.__module__, class_or_function.__name__)
