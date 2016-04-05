from django.db import models


class ProfileManager(models.Manager):
    def create_new_profile_for_driver(self, driver_obj):
        driver_driving_data = driver_obj.driving_data.data
        return driver_driving_data