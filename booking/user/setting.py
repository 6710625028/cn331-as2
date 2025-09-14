INSTALLED_APPS = [
    # ...
    ’django.contrib.staticfiles‘,
    ’crispy_forms‘,
    ’crispy_bootstrap5‘,
    ’bookings‘,
]
CRISPY_ALLOWED_TEMPLATE_PACKS = ”bootstrap5“
CRISPY_TEMPLATE_PACK = ”bootstrap5“

STATIC_URL = ’/static/‘

LOGIN_URL = ’login‘
LOGIN_REDIRECT_URL = ’/‘
LOGOUT_REDIRECT_URL = ’login‘


