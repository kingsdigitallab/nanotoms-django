from .base import *  # noqa

ALLOWED_HOSTS = ['nanotoms.kdl.kcl.ac.uk']

INTERNAL_IPS = INTERNAL_IPS + ['']

DATABASES = {
    'default': {
        'ENGINE': db_engine,
        'NAME': 'app_nanotoms_liv',
        'USER': 'app_nanotoms',
        'PASSWORD': '',
        'HOST': ''
    },
}

SECRET_KEY = ''
