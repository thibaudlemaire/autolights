import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), ''))
os.environ["DJANGO_SETTINGS_MODULE"] = "user_interface.autolights.settings"
import django
# Init Django
django.setup()