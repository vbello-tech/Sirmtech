from .settings import *

# settings for production server.

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + THIRD_PARTY_APPS

