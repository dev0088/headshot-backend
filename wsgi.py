"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

# import os

# from django.core.wsgi import get_wsgi_application
# from dj_static import Cling

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# application = Cling(get_wsgi_application())

import os

# for only local development env, comment. but uncomment on production server
#site.addsitedir("/home/centos/shiptalent/backend/env3/lib/python3.6/site-packages")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

from django.core.wsgi import get_wsgi_application
from dj_static import Cling

application = Cling(get_wsgi_application())