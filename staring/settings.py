"""
Django settings for staring project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from pathlib import Path
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-==cc*=kn9y#rqj%ixh+wi%&34_-k)o!h0!gn8pch)eytjcfefy'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

AUTH_USER_MODEL = 'staring.User'

DOMAIN_NAME = "https://star.ourcv.net"

CSRF_TRUSTED_ORIGINS = ["star.ourcv.net"]

# Application definition

INSTALLED_APPS = [
    # 'grappelli',
    # 'filebrowser',

    # 'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # installed apps
    'django_countries',
    'ckeditor',
    'ckeditor_uploader',
    'widget_tweaks',
    'guardian',
    'modeltranslation',
    'django_user_agents',

    # customer apps
    'staring',
    'customer',
    'admin',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware'
]

ROOT_URLCONF = 'staring.urls'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'guardian.backends.ObjectPermissionBackend',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'staring.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'star',
        'USER': 'root',
        'PASSWORD': 'xinghuan',
        'HOST': '192.248.163.9',
        'PORT': '3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

X_FRAME_OPTIONS = 'SAMEORIGIN'


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGES = (
    ('zh-hans', '简体中文'),
    ('en-us', 'English')
)

MODELTRANSLATION_LANGUAGES = ('zh-hans', 'en-us')

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)
STATIC_ROOT = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = 'media/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CKEditor Setting
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_JQUERY_URL = "https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': [
            {"name": "tools", "items": ["Maximize", "ShowBlocks"]},
            {"name": "document", "items": ["Source", "-", "Save", "Print"]},
            {"name": "clipboard", "items": ["Copy", "Cut", "Paste", "PasteText", "PasteFromWord", "Undo", "Redo"]},
            {"name": "link", "items": ["Link", "Unlink", "Anchor"]},
            {"name": "insert",
             "items": ["Image", "Table", "HorizontalRule", "Smiley", "SpecialChar", "PageBreak", "Iframe"]},
            "/",
            {"name": "basicstyles", "items": ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-',
                                              'RemoveFormat']},
            {"name": "paragraph",
             "items": ["NumberedList", "BulletedList", "-", "Outdent", "Indent", "-", "Blockquote", "CreateDiv", "-",
                       "JustifyLeft", "JustifyCenter", "JustifyRight", "JustifyBlock", "-", "BidiLtr", "BidiRtl",
                       "Language"]},
            {"name": "styles", "items": ["Styles", "Format", "Font", "FontSize"]},
            {"name": "colors", "items": ["TextColor", "BGColor"]},
        ],
        'tabSpaces': 4,
        'width': '100%',
        'extraPlugins': ','.join([
            "uploadimage",
            "div",
            "autolink",
            "autoembed",
            "embedsemantic",
            "autogrow",
            "widget",
            "lineutils",
            "clipboard",
            "dialog",
            "dialogui",
            "elementspath",
        ])
    },
}
