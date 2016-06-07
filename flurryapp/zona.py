import django
django.setup()

from flurryapp.models import *

Driver.objects.check_for_duplicate_rides()