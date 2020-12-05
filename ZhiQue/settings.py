"""
Django settings for ZhiQue project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""
import datetime
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('ZHIQUE_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if os.environ.get('ZHIQUE_DEBUG') == 'True' else False

ALLOWED_HOSTS = os.environ.get('ZHIQUE_ALLOWED_HOSTS').split(',')


# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'rest_framework',
    'rest_framework.authtoken',
    'drf_yasg2',
    'corsheaders',
    'account.apps.AccountConfig',
    'oauth.apps.OAuthConfig',
    'customize.apps.CustomizeConfig',
    'yuque.apps.YuQueConfig',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'ZhiQue.middleware.DataFormatMiddleware',
]

ROOT_URLCONF = 'ZhiQue.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
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

WSGI_APPLICATION = 'ZhiQue.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('ZHIQUE_DB_NAME'),
        'USER': os.environ.get('ZHIQUE_DB_USER'),
        'PASSWORD': os.environ.get('ZHIQUE_DB_PASSWORD'),
        'HOST': os.environ.get('ZHIQUE_DB_HOST'),
        'PORT': os.environ.get('ZHIQUE_DB_PORT'),
        'OPTIONS': {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://{url}:{port}/0'.format(
            url=os.environ.get('ZHIQUE_REDIS_HOST'),
            port=os.environ.get('ZHIQUE_REDIS_PORT')
        ),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "PASSWORD": '',
        },
    },
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = 'account.User'

LOGIN_URL = '/oauth/login'
LOGOUT_URL = '/oauth/logout'

AUTHENTICATION_BACKENDS = (
    'oauth.authentication.EmailOrUsernameModelBackend',
)


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

STATIC_ROOT = os.path.join(BASE_DIR, 'collectedstatic')

# Settings for REST framework are all namespaced in the REST_FRAMEWORK setting.
# https://www.django-rest-framework.org/api-guide/settings/
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
    'DEFAULT_VERSION': 'v1',
    'ALLOWED_VERSIONS': ['v1', 'v2'],
    'DEFAULT_PAGINATION_CLASS': 'ZhiQue.utils.Pagination',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'EXCEPTION_HANDLER': 'ZhiQue.utils.zhique_exception_handler'
}

SERVICE_BASE_URL = os.environ.get('ZHIQUE_SERVICE_BASE_URL')
FRONT_BASE_URL = os.environ.get('ZHIQUE_FRONT_BASE_URL')

CORS_ORIGIN_WHITELIST = [
    FRONT_BASE_URL
]

# email
# https://docs.djangoproject.com/en/3.0/topics/email/
# 邮件系统设置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# 是否使用TLS安全传输协议
EMAIL_USE_TLS = False
# 是否使用SSL加密，qq企业邮箱要求使用
EMAIL_USE_SSL = True
# SMTP服务器
EMAIL_HOST = 'smtp.ym.163.com'
# SMTP服务器端口
EMAIL_PORT = 994
# 发件人
EMAIL_HOST_USER = '系统通知'
# 默认发件人邮箱
DEFAULT_FROM_EMAIL = 'notice@xuzhao.xin'
# POP3/SMTP 授权码
# IMAP/SMTP 授权码
EMAIL_HOST_PASSWORD = os.environ.get('ZHIQUE_EMAIL_HOST_PASSWORD')

# 网站异常通知
ADMINS = [('admin', 'admin@zhique.com')]

# logging
# https://docs.djangoproject.com/en/3.0/topics/logging/
LOGGING = {
    'version': 1,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    }
}
