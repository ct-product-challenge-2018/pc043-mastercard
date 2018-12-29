from asine_me.settings.base import *

# Override base settings for dev
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'asinemeteam@gmail.com'