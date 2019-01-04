from asine_me.settings.base import *

# Override base settings for prod
SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = False

STATIC_URL = '/static/'
STATIC_ROOT = '/static_files/'

ALLOWED_HOSTS = [
    '0.0.0.0',
    '206.81.8.163',
    'asine.me',
]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'asinemeteam@gmail.com'
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
EMAIL_PORT = 587
EMAIL_USE_TLS = True
