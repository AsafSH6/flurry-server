from __future__ import unicode_literals
import django

django.setup()

from flurryapp.models import *
import requests as req
import getpass

SERVER_API_URL = 'http://54.152.123.228/api/v1/flurry/'


def delete_current_db():
    print 'deleted users', User.objects.all().delete()
    print 'deleted data drivers', DataDriver.objects.all().delete()


def import_all_drivers_and_their_data():
    all_drivers = req.get(SERVER_API_URL + 'drivers/').json()

    for driver in all_drivers:
        driver_driving_data = req.get(driver['driving_data']).json()
        driver_driving_data = DataDriver.objects.create(data=driver_driving_data['data'])

        user = User.objects.create_user(username=driver['user']['username'], password='1')

        new_driver = Driver.objects.create(user=user,
                                           name=driver['name'],
                                           driving_data=driver_driving_data)
        print 'created', new_driver


if __name__ == '__main__':
    user = getpass.getuser()
    if user is not 'ubuntu':
        delete_current_db()
        import_all_drivers_and_their_data()

