from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from flurryapp.managers.profile_manager import ProfileManager


class DataDriver(models.Model):
    data = JSONField(default=[])

    def save(self, *args, **kwargs):
        super(DataDriver, self).save(*args, **kwargs)
        return self


class Driver(models.Model):
    user = models.ForeignKey(User, related_name='drivers')
    name = models.CharField(max_length=255)
    creation_date = models.DateField(auto_now_add=True)
    driving_data = models.ForeignKey(DataDriver, related_name='driver')

    def __unicode__(self):
        return u'{id}--{name}--{date}'.format(id=self.id,
                                              name=self.name,
                                              date=self.creation_date.strftime("%d/%m/%y"))

    def save(self, *args, **kwargs):
        try:
            self.driving_data
        except DataDriver.DoesNotExist:
            self.driving_data = DataDriver().save()
        super(Driver, self).save(*args, **kwargs)
        return self


class Car(models.Model):
    manufacturer = models.CharField(max_length=255)
    production_year = models.IntegerField()
    model = models.CharField(max_length=1024)  # GOLF GTI 1800
    owner = models.ForeignKey(Driver, related_name='cars')

    def __unicode__(self):
        return u'{manufacturer}, {production_year}, {model}'.format(manufacturer=self.manufacturer,
                                                                    production_year=self.production_year,
                                                                    model=self.model)

    def save(self, *args, **kwargs):
        super(Car, self).save(*args, **kwargs)
        return self


class Profile(models.Model):
    driver = models.ForeignKey(Driver, related_name='profiles')
    avg_rpm = models.FloatField(null=True)

    objects = ProfileManager()

    def __unicode__(self):
        return u'Profile analysis of driver: {name}'.format(name=self.driver.name)

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        return self
