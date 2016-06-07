from __future__ import unicode_literals
import django
import sys

django.setup()

from flurryapp.models import *
from flurryapp.utils.maximum_limitation_of_speed import MaximumLimitationOfSpeedAPIClient


def insert_maximum_speed_limitation_if_missed(driver_id):
    speed_limit_client = MaximumLimitationOfSpeedAPIClient()
    driver = Driver.objects.get(id=driver_id)
    print driver

    driver_driving_data = driver.driving_data.data

    for ride_index in xrange(len(driver_driving_data)):
        for data_unit_index, data_unit in enumerate(driver[ride_index]):
            if 'maximum_limition_of_speed' not in data_unit:
                driver[ride_index][data_unit_index]['maximum_limition_of_speed'] = speed_limit_client.get_maximum_limitation_of_speed_in_kmph(
                    lat=data_unit['gps']['lat'],
                    lon=data_unit['gps']['lon']
                )
                print 'inserted'
            print ride_index, data_unit_index
    driver.save()


if __name__ == '__main__':
    if len(sys.argv) is not 2:
        print 'missing driver id'
        quit()

    insert_maximum_speed_limitation_if_missed(driver_id=sys.argv[1])
