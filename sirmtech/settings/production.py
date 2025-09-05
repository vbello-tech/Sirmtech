from .settings import *

# settings for production server.

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
#
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

# cloudinary api key
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': config('CLOUD_NAME'),
    'API_KEY': config('API_KEY'),
    'API_SECRET': config('API_SECRET'),
}

# storage settings
STORAGES = {
    "default": {
        "BACKEND": 'cloudinary_storage.storage.MediaCloudinaryStorage',
        # "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        # "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

CSRF_TRUSTED_ORIGINS = ['https://sirmtech.fly.dev', '127.0.0.1', 'localhost']

CORS_ORIGIN_ALLOW_ALL = True

SECURE_SSL_REDIRECT = False

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

SECURE_BROWSER_XSS_FILTER = True

