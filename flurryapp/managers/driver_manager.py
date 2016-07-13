from __future__ import unicode_literals

from django.db import models

from flurryapp.utils.maximum_limitation_of_speed import MaximumLimitationOfSpeedAPIClient


class DriverManager(models.Manager):
    def __init__(self):
        super(DriverManager, self).__init__()
        try:
            self.speed_limit_client = MaximumLimitationOfSpeedAPIClient()
        except ValueError as e:
            self.speed_limit_client = None

    def append_new_driving_data(self, driver_id, driving_data):
        '''
        driving_data format:
         [
             {
             time: 123,
             speed: 123,
             rpm: 123,
             gps: {
                    lat: 123,
                    lon: 123
                }
             },
             {
             time: 124,
             speed: 123,
             rpm: 123,
             gps: {
                    lat: 123,
                    lon: 123
                }
             },
             ...
         ]
        '''
        driver = self.get(id=driver_id)
        if self.speed_limit_client is not None:
            for data_unit_index, data_unit in enumerate(driving_data):
                self.__append_maximum_limitation_of_speed(data_unit)

        driver.driving_data.data.append(driving_data)
        driver.driving_data.save()

    def __append_maximum_limitation_of_speed(self, data_unit):
        data_unit['maximum_limition_of_speed'] = self.speed_limit_client.get_maximum_limitation_of_speed_in_kmph(
            lat=data_unit['gps']['lat'],
            lon=data_unit['gps']['lon']
        )

    def check_for_duplicate_rides(self):
        for driver in self.all():
            print 'checking duplicate rides for driver:', driver.name

            num_of_rides = len(driver)
            print 'driver have', num_of_rides, 'rides'

            for i in xrange(num_of_rides - 1):
                if all(driver[i][j] == driver[i + 1][j] for j in xrange(min(len(driver[i]), len(driver[i + 1])))):
                    print '*', i, '==', i + 1, '*'

            print '\n'

    def check_for_rides_with_closed_gps(self):
        for driver in self.all():
            print 'checking rides with closed gps:', driver.name

            num_of_rides = len(driver)
            print 'driver have', num_of_rides, 'rides'

            for ride_index, ride in enumerate(driver):
                if all(data_unit['maximum_limition_of_speed'] < 0 for data_unit in ride):
                    print 'ride {ride_index} had closed GPS'.format(ride_index=ride_index)

            print '\n'

