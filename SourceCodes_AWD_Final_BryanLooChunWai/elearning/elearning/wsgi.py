# import libraries and modules
import os
from django.core.wsgi import get_wsgi_application

# set up os from elearning settings file
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "elearning.settings")

# define application using WSGI
application = get_wsgi_application()
