from __future__ import unicode_literals
from django.db import models
import math

from flurryapp.utils.maximum_limitation_of_speed import MaximumLimitationOfSpeedAPIClient


MILLISECOND_TO_MINUTE = 60000

DEFAULT_VALUES_TO_CHECK = ['speed', 'rpm']#, 'throttle', 'accelerator']


class DriverManager(models.Manager):
    def __init__(self):
        super(DriverManager, self).__init__()
        self.speed_limit_client = MaximumLimitationOfSpeedAPIClient()

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
        for data_unit_index, data_unit in enumerate(driving_data):
            self.__append_maximum_limitation_of_speed(data_unit)

        driver.driving_data.data.append(driving_data)
        driver.driving_data.save()

    def check_for_duplicate_rides(self):
        all_drivers = self.all()
        for driver in all_drivers:
            print 'checking driver:', driver.name

            num_of_rides = len(driver)
            print 'driver have', num_of_rides, 'rides'
            for i in xrange(num_of_rides - 1):
                if all(driver[i][j] == driver[i + 1][j] for j in xrange(min(len(driver[i]), len(driver[i + 1])))):
                    print '*', i, '==', i + 1, '*'
                # else:
                #     print i, '=/=', i + 1
            print '\n'

    def extract_features(self, percents_of_driving_data=100, offset_from_beginning=0):
        '''
        extracting features of every driver in the DB
        :return: dict of driver name as key and list of features as value
        '''
        driver_name_to_list_of_features_dict = dict()
        # for driver in [self.get(id=49)]:
        for driver in self.all():
            if len(driver) is not 0:
                print 'checking driver', driver.name
                driver_name_to_list_of_features_dict[driver.name] = list()

                driver_driving_data_merged = reduce(lambda x, y: x + y, driver.driving_data.data)
                num_of_data_units = len(driver_driving_data_merged)
                print 'num of data units', num_of_data_units

                beginning = int(num_of_data_units / 100.0 * offset_from_beginning)
                end = int((num_of_data_units - beginning) / 100.0 * percents_of_driving_data)
                print 'beginning', beginning
                print 'end', end

                sliced_driving_data = driver_driving_data_merged[beginning:end]
                print 'number of sliced data', len(sliced_driving_data)

                driver_name_to_list_of_features_dict[driver.name] += self.__average_per_minute(sliced_driving_data)
                driver_name_to_list_of_features_dict[driver.name].append(self.__calculate_over_max_speed_precentage(sliced_driving_data))
                driver_name_to_list_of_features_dict[driver.name].append(self.__average_throttle_pressed_per_minitue(sliced_driving_data))

                print '\n'

        print driver_name_to_list_of_features_dict
        return driver_name_to_list_of_features_dict

    def __average_per_minute(self, data, keys=DEFAULT_VALUES_TO_CHECK):
        beginning_of_the_minute = int(data[0]['time'])
        dict_of_key_to_list_of_lists_of_values_per_minute = {key: [[]] for key in keys}

        for data_unit in data:
            data_unit_time = int(data_unit['time'])
            if (beginning_of_the_minute + MILLISECOND_TO_MINUTE) - data_unit_time < 0:
                beginning_of_the_minute = data_unit_time
                for key in keys:
                    dict_of_key_to_list_of_lists_of_values_per_minute[key].append([])
            for key in keys:
                dict_of_key_to_list_of_lists_of_values_per_minute[key][-1].append(float(data_unit[key]))

        for key in keys:
            list_of_lists_of_values_per_minute = dict_of_key_to_list_of_lists_of_values_per_minute[key]
            average_of_values_per_minute = sum(sum(values_per_minute) / len(values_per_minute) for values_per_minute in list_of_lists_of_values_per_minute)
            dict_of_key_to_list_of_lists_of_values_per_minute[key] = average_of_values_per_minute / len(list_of_lists_of_values_per_minute)

        print dict_of_key_to_list_of_lists_of_values_per_minute
        return dict_of_key_to_list_of_lists_of_values_per_minute.values()

    def __calculate_over_max_speed_precentage(self, data, minimum_speed=0):
        a = [float(data_unit['speed']) > float(data_unit['maximum_limition_of_speed']) for data_unit in data if float(data_unit['speed']) > minimum_speed]
        return float(sum(a)) / len(a)

    def __average_throttle_pressed_per_minitue(self, data):
        beginning_of_the_minute = int(data[0]['time'])
        list_of_presses_per_minute = [0]

        speed_before_was_zero = False
        for data_unit_index in xrange(len(data) - 1):
            data_unit_time = int(data[data_unit_index]['time'])
            if (beginning_of_the_minute + MILLISECOND_TO_MINUTE) - data_unit_time < 0:
                beginning_of_the_minute = data_unit_time
                list_of_presses_per_minute.append(0)

            # throttle pressed and the current speed is not 0 or the speed before was not zero
            if not (data[data_unit_index]['speed'] == '0' and speed_before_was_zero) and data[data_unit_index]['throttle'] < data[data_unit_index + 1]['throttle']:
                list_of_presses_per_minute[-1] += 1

            speed_before_was_zero = data[data_unit_index]['speed'] == '0'

        print list_of_presses_per_minute
        return float(sum(list_of_presses_per_minute)) / len(list_of_presses_per_minute)

    def __append_maximum_limitation_of_speed(self, data_unit):
        data_unit['maximum_limition_of_speed'] = self.speed_limit_client.get_maximum_limitation_of_speed_in_kmph(
            lat=data_unit['gps']['lat'],
            lon=data_unit['gps']['lon']
        )

