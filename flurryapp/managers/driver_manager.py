from __future__ import unicode_literals
from django.db import models
from sklearn.preprocessing import MinMaxScaler
import numpy as np

from flurryapp.utils.maximum_limitation_of_speed import MaximumLimitationOfSpeedAPIClient


MILLISECOND_TO_MINUTE = 60000
DRASTIC_SPEED_THRESHOLD = 3
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

    def extract_features(self):
        '''
        extracting features of every driver in the DB
        :return: dict of driver name as key and list of features as value
        '''
        driver_name_to_list_of_features_dict = dict()
        # for driver in [self.get(id=79)]:
        for driver in self.all():
            if len(driver) is not 0:
                driver_name_to_list_of_features_dict[driver.name] = list()

                driver_driving_data = driver.driving_data.data

                for ride in driver_driving_data:
                    # self.__preprocessor(ride)
                    ride_as_vector = []
                    ride_as_vector += self.__average_per_minute(ride)
                    ride_as_vector.append(self.__calculate_over_max_speed_precentage(ride))
                    ride_as_vector.append(self.__average_throttle_pressed_per_minitue(ride))
                    ride_as_vector.append(self.__calculate_average_drastic_speed_changes_per_minute(ride))
                    driver_name_to_list_of_features_dict[driver.name].append(ride_as_vector)

        # for driver in driver_name_to_list_of_features_dict:
        #     print 'driver:', driver
        #     print driver_name_to_list_of_features_dict[driver]

        return driver_name_to_list_of_features_dict

    # def __preprocessor(self, data):
    #     min_max_scaler = MinMaxScaler()
    #     vals = [float(data_unit['throttle']) for data_unit in data]
    #     scaled = min_max_scaler.fit_transform(vals)
    #

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

        # print dict_of_key_to_list_of_lists_of_values_per_minute
        return dict_of_key_to_list_of_lists_of_values_per_minute.values()

    def __calculate_over_max_speed_precentage(self, data, minimum_speed=0):
        a = [float(data_unit['speed']) > float(data_unit['maximum_limition_of_speed']) for data_unit in data if float(data_unit['speed']) > minimum_speed]
        return float(sum(a)) / len(a) if len(a) > 0 else 0

    def __calculate_average_drastic_speed_changes_per_minute(self, data, threshold=DRASTIC_SPEED_THRESHOLD):
        beginning_of_the_minute = int(data[0]['time'])
        list_of_lists_of_drastic_changes_per_minute = [[]]

        last_speed = int(data[0]['speed'])
        for data_unit in data:
            data_unit_time = int(data_unit['time'])
            if (beginning_of_the_minute + MILLISECOND_TO_MINUTE) - data_unit_time < 0:
                list_of_lists_of_drastic_changes_per_minute.append([])

            current_speed = int(data_unit['speed'])
            if threshold < abs(current_speed - last_speed):
                change_to_calculate = current_speed - threshold - last_speed if current_speed > last_speed else last_speed - threshold - current_speed
                change_to_calculate = 1
                list_of_lists_of_drastic_changes_per_minute[-1].append(change_to_calculate)  # the drastic change itself

            last_speed = current_speed
        list_of_avg_for_each_list = lambda l: [float(sum(sublist)) / len(sublist) if len(sublist) > 0 else 0 for sublist in l]
        avg_of_each_list_of_drastic_speed_change_per_minute = list_of_avg_for_each_list(l=list_of_lists_of_drastic_changes_per_minute)
        return float(sum(avg_of_each_list_of_drastic_speed_change_per_minute)) / len(avg_of_each_list_of_drastic_speed_change_per_minute)

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

        # print list_of_presses_per_minute
        return float(sum(list_of_presses_per_minute)) / len(list_of_presses_per_minute)

    def __append_maximum_limitation_of_speed(self, data_unit):
        data_unit['maximum_limition_of_speed'] = self.speed_limit_client.get_maximum_limitation_of_speed_in_kmph(
            lat=data_unit['gps']['lat'],
            lon=data_unit['gps']['lon']
        )

