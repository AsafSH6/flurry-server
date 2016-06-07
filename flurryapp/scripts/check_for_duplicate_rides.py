import django
django.setup()

from flurryapp.models import *


if __name__ == '__main__':
    Driver.objects.check_for_duplicate_rides()