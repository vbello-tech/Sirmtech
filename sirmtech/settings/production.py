from .settings import *

# settings for production server.

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('DB_DATABASE'),
        'USER': config('DB_USERNAME'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}

# db.sqlite3 in production
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / 'db.sqlite3',
#         "OPTIONS": {
#             "transaction_mode": "IMMEDIATE",
#             "timeout": 5,  # seconds
#             "init_command": """
#                 PRAGMA journal_mode=WAL;
#                 PRAGMA synchronous=NORMAL;
#                 PRAGMA mmap_size=134217728;
#                 PRAGMA journal_size_limit=27103364;
#                 PRAGMA cache_size=2000;
#             """,
#         },
#     },
# }

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

