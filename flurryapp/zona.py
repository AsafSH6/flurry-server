import django
django.setup()

from flurryapp.models import *

Driver.objects.extract_features()
