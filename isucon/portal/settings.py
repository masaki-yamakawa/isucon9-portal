"""
Django settings for portal project.

Generated by 'django-admin startproject' using Django 2.2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import datetime
import os

from isucon.portal import utils as portal_utils

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^lz^(m-uy*2htu^fvolbhj!(pmu$x4*c@30s2i)70e=zt_vyai'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'isucon.portal',
    'isucon.portal.authentication',
    'isucon.portal.contest',
    'isucon.portal.contest.alibaba',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.humanize',
    'django.contrib.staticfiles',
    'rest_framework',
    'social_django',
    'widget_tweaks',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTHENTICATION_BACKENDS = (
    'social_core.backends.github.GithubOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)


ROOT_URLCONF = 'isucon.portal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'isucon.portal.contest.context_processors.settings_url',
            ],
        },
    },
]

WSGI_APPLICATION = 'isucon.portal.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ATOMIC_REQUESTS': True,
    }
}

AUTH_USER_MODEL = "authentication.User"


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'ja-jp'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

LOGIN_URL = "login"

# アイコンの最大アップロードファイルサイズ(5MB)
MAX_UPLOAD_SIZE = 5242880

# アプリケーション固有設定
MEDIA_ROOT = 'media/'
MEDIA_URL = '/media/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {},
    'handlers': {
        'slack_admins': {
            'level': 'ERROR',
            'filters': [],
            'class': 'isucon.portal.logging.SlackExceptionHandler',
        },
        'console': {
            'level': 'INFO',
            'filters': [],
            'class': 'logging.StreamHandler',
        },
    },
    'formatters': {
        'simple': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[%(server_time)s] %(message)s a',
        }
    },
    'loggers': {
        'django': {
            'level': 'INFO',
            'handlers': ['console'],
        },
        'isucon': {
            'level': 'INFO',
            'handlers': ['console'],
        },
    },
}


# 登録期間
REGISTRATION_START_AT = portal_utils.get_utc_datetime(2019, 7, 1, 9, 0, 0)
REGISTRATION_END_AT = portal_utils.get_utc_datetime(2019, 10, 25, 9, 0, 0)

# コンテスト開催期間
# 日付
CONTEST_DATES = [
    datetime.date(2019, 9, 3),
    datetime.date(2019, 9, 3)
]

# 時刻
CONTEST_START_TIME = portal_utils.get_utc_time(9, 0, 0)
CONTEST_END_TIME = portal_utils.get_utc_time(18, 0, 0)

# Github認証に使うトークン
# TODO: 入れ替える
SOCIAL_AUTH_GITHUB_KEY = '8ad74d7452d59b6d5572'
SOCIAL_AUTH_GITHUB_SECRET = '3682fb62f9623c93cfc5fa1c2c79cbe9e539e016'

BENCHMARK_ABORT_TIMEOUT_SEC = 300

# チームに所属できる最大人数
MAX_TEAM_MEMBER_NUM = 3
# 最大チーム数
MAX_TEAM_NUM = 600

# チームパスワードとして使う文字群
PASSWORD_LETTERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*'
# チームパスワードの文字数
PASSWORD_LENGTH = 20

# Redis
REDIS_HOST = '127.0.0.1'
RANKING_TOPN = 30

# Slack
SLACK_ENDPOINT_URL = "https://hooks.slack.com/services/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"


# Alibaba Cloud
ALIBABA_ACCESS_KEY_ID = "LTAICojzw6sk7nJV"
ALIBABA_ACCESS_KEY_SECRET = "UuBcfezGolj9GGoimz9wopcalu9dEG"

# 外部リンク
MANUAL_URL = '' # TODO:
REGULATION_URL = '' # TODO:
DISCORD_URL = '' # TODO:
ISUCON_OFFICIAL_URL = 'http://isucon.net/'
TWITTER_URL = 'https://twitter.com/isucon_official'
TERM_URL = 'http://isucon.net/archives/53567239.html'
