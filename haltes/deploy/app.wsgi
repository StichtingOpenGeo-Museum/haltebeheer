import os, sys
import site

# CHANGE THIS: set your virtual environment path here  
site.addsitedir('/home/joel/envs/fixmyhalte/lib/python2.7/site-packages')
# END CHANGE

sys.path.insert(0, os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir, os.pardir)))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir)))

from django.core.handlers.wsgi import WSGIHandler
os.environ["DJANGO_SETTINGS_MODULE"] = "haltes.settings"
application = WSGIHandler()