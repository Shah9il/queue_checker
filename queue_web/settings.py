import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ksuk*t8b-k-gkg-q@tq_66#5ca=&irkvk(5m^!2!zy&$=roz25'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'queue_checker',
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

ROOT_URLCONF = 'queue_web.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'queue_web.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

if os.environ.get('DJANGO_ENV') == 'TEST':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
# else:
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.mysql',
#             'NAME': os.getenv("DBNAME"),
#             'USER': os.getenv("DBUSER"),
#             'PASSWORD': os.getenv("DBPASSWORD"),
#             'HOST': os.getenv("DBHOST"),
#             'PORT': os.getenv("DBPORT"),
#             'OPTIONS': {
#             'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
#             'charset': 'utf8mb4',
#             },
#         }
#     }



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


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False if DEBUG else True,  # Whether to disable loggers that already exist
    'formatters': {  # Format for displaying log information
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)s %(message)s'
            # "class": "pythonjsonlogger.jsonlogger.JsonFormatter"
        },
        'simple': {
            'format': '%(levelname)s %(asctime)s %(module)s %(funcName)s %(lineno)d %(message)s'
            # "class": "pythonjsonlogger.jsonlogger.JsonFormatter"
        },  # Logging Level+Time Date+Module Name+Function Name+Line Number+Logging Message
    },
    'filters': {  # Filter logs
        'require_debug_true': {  # django does not output logs until debug mode
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {  # Log Processing Method
        'console': {  # Output log to terminal
            'level': 'DEBUG' if DEBUG else 'INFO',
            'filters': ['require_debug_true'],  # debug is true before output
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'info': {  # Output log to file
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': "info.log",  # Location of log files
            'maxBytes': 300 * 1024 * 1024,  # 300M Size
            'backupCount': 10,
            'formatter': 'verbose',
            'encoding': 'utf-8'
        },
        'demo': {   # Specially define a log to collect specific information
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',  # Save to file, auto-cut
            'filename': "demo.log",
            'maxBytes': 1024 * 1024 * 50,  # Log size 50M
            'backupCount': 5,
            'formatter': 'verbose',
            'encoding': "utf-8"
        },

    },
    'loggers': {  # Logger
        "django": {        # The default logger application is configured as follows
            "handlers": ["info", "console"],
            "propagate": True,
            "level": "INFO"
        },
        'demo_log': {      # The logger named'demo'is also handled separately
            'handlers': ['demo'],
            "propagate": True,
            'level': 'INFO',
        },
    }
}

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
