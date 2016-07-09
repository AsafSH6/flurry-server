from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField
from flurryapp.managers.driver_manager import DriverManager


class DataDriver(models.Model):
    data = JSONField(default=[])

    def __unicode__(self):
        return 'id: {pk}'.format(pk=self.pk)

    def __getitem__(self, item):
        return self.data[item]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __len__(self):
        return len(self.data)

    def save(self, *args, **kwargs):
        super(DataDriver, self).save(*args, **kwargs)
        return self


class Driver(models.Model):
    user = models.ForeignKey(User, null=True, related_name='drivers')
    name = models.CharField(max_length=255)
    creation_date = models.DateField(auto_now_add=True)
    driving_data = models.ForeignKey(DataDriver, related_name='driver', null=True)

    objects = DriverManager()

    def __unicode__(self):
        return u'{id}--{name}--{date}'.format(id=self.id,
                                              name=self.name,
                                              date=self.creation_date.strftime("%d/%m/%y"))

    def __getitem__(self, item):
        return self.driving_data[item]

    def __setitem__(self, key, value):
        self.driving_data[key] = value

    def __len__(self):
        return len(self.driving_data)

    def save(self, *args, **kwargs):
        if self.driving_data is None:
            self.driving_data = DataDriver.objects.create()
        super(Driver, self).save(*args, **kwargs)
        self.driving_data.save()
        return self
