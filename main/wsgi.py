import sys
import os

PATH = "/var/www/sydneymenu/"
sys.path.append(PATH + 'main/')
sys.path.append(PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
os.environ['PYTHON_EGG_CACHE'] = '/tmp'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
