from __future__ import unicode_literals

from time import sleep

from django.db import models
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import logging

from flurryapp.utils.maximum_limitation_of_speed import MaximumLimitationOfSpeedAPIClient

logging.basicConfig(filename='test.log', level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())


MILLISECOND_TO_MINUTE = 60000
DRASTIC_SPEED_THRESHOLD = 3
DEFAULT_VALUES_TO_CHECK = ['speed', 'rpm']#, 'throttle', 'accelerator']
VALUES_TO_SCALE = ['throttle', 'rpm']

SLEEP_TIME = 0


def SLEEP(time=SLEEP_TIME): sleep(time)


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
        extracting features of every driver in DB
        :return: dict of driver name as key and list of features as value
        '''
        logging.debug('** EXTRACT FEATURES **\n\n')
        SLEEP()

        driver_name_to_list_of_features_dict = dict()
        # for driver in [self.get(id=85)]:
        for driver in self.all():
            if len(driver) > 1 and driver.name != 'Test Driver':
                logging.info('Extracting features for driver: ' + unicode(driver))
                SLEEP()

                driver_name_to_list_of_features_dict[driver.name] = list()

                driver_driving_data = driver.driving_data.data

                logging.info('Driver has ' + unicode(len(driver_driving_data) + 1) + ' rides')
                SLEEP()

                for ride_index, ride in enumerate(driver_driving_data):
                    logging.debug('\nBuilding features vector for ride: ' + unicode(ride_index + 1))
                    logging.info('Ride has ' + unicode(len(ride)) + ' data units')
                    SLEEP()

                    ride = self.__preprocessor(ride)
                    SLEEP()
                    ride_as_vector = []
                    ride_as_vector += self.__average_per_minute(ride)
                    SLEEP()
                    ride_as_vector.append(self.__calculate_over_max_speed_precentage(ride))
                    SLEEP()
                    ride_as_vector.append(self.__average_throttle_pressed_per_minitue(ride))
                    SLEEP()
                    ride_as_vector.append(self.__calculate_average_drastic_speed_changes_per_minute(ride))
                    SLEEP()
                    driver_name_to_list_of_features_dict[driver.name].append(ride_as_vector)
                    SLEEP()

        return driver_name_to_list_of_features_dict

    def __preprocessor(self, data):
        logging.debug('\n~ Running Preprocessor ~')

        min_max_scaler = MinMaxScaler()
        dict_of_scaled_values = dict()

        for value in VALUES_TO_SCALE:
            logging.debug('Scaling ' + unicode(value).upper())
            values_iterable = (data_unit[value] for data_unit in data if data_unit[value] != '-1')

            # values_iterable = (data_unit[value] for data_unit in data)

            values_arr = np.fromiter(values_iterable, np.float)

            values_scaled = min_max_scaler.fit_transform(np.reshape(values_arr, (-1, 1))).reshape(values_arr.size)

            logging.debug('Minimum value: ' + unicode(min_max_scaler.data_min_[0]) + ', Maximum value: ' + unicode(min_max_scaler.data_max_[0]))

            dict_of_scaled_values[value] = values_scaled

        # offset for skipped values since value == -1
        value_to_offset = {value: 0 for value in VALUES_TO_SCALE}

        for index in xrange(values_scaled.size):
            for value, values_scaled in dict_of_scaled_values.iteritems():
                offset = value_to_offset[value]
                if data[index + offset][value] != '-1':  # skip this data unit
                    data[index + offset][value] = values_scaled[index]

                else:
                    value_to_offset[value] += 1

        return data

    def __average_per_minute(self, data, keys=DEFAULT_VALUES_TO_CHECK):
        logging.debug('\n~ Average ' + ', '.join(keys).upper() + ' Per Minute ~')

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

            logging.debug('values per minute of: ' + key.upper() + ' ' + unicode(list_of_lists_of_values_per_minute))

            avg = lambda l: float(sum(l)) / len(l) if len(l) > 0 else 0
            average_of_values_per_minute = sum(avg(values_per_minute) for values_per_minute in list_of_lists_of_values_per_minute)
            dict_of_key_to_list_of_lists_of_values_per_minute[key] = average_of_values_per_minute / len(list_of_lists_of_values_per_minute)

            logging.debug('average per minute: ' + unicode(dict_of_key_to_list_of_lists_of_values_per_minute[key]))

        # print dict_of_key_to_list_of_lists_of_values_per_minute
        return dict_of_key_to_list_of_lists_of_values_per_minute.values()

    def __calculate_over_max_speed_precentage(self, data, minimum_speed=0):
        logging.debug('\n~ Over Maximum Speed Limitation Precentage ~')

        a = [float(data_unit['speed']) > float(data_unit['maximum_limition_of_speed']) for data_unit in data if float(data_unit['speed']) > minimum_speed]
        over_max_speed = float(sum(a)) / len(a) if len(a) > 0 else 0
        logging.debug('Driver had passed the maximum limitation ' + unicode(over_max_speed * 100) + '% of the time')
        return over_max_speed

    def __calculate_average_drastic_speed_changes_per_minute(self, data, threshold=DRASTIC_SPEED_THRESHOLD):
        logging.debug('Calculate Average Drastic Speed Change')
        logging.info('Threshold = ' + unicode(threshold))

        beginning_of_the_minute = int(data[0]['time'])
        list_of_lists_of_drastic_changes_per_minute = [[]]

        last_speed = int(data[0]['speed'])
        for data_unit in data:
            data_unit_time = int(data_unit['time'])
            if (beginning_of_the_minute + MILLISECOND_TO_MINUTE) - data_unit_time < 0:
                list_of_lists_of_drastic_changes_per_minute.append([])

            current_speed = int(data_unit['speed'])
            if threshold < abs(current_speed - last_speed):
                # change_to_calculate = current_speed - threshold - last_speed if current_speed > last_speed else last_speed - threshold - current_speed
                change_to_calculate = 1
                list_of_lists_of_drastic_changes_per_minute[-1].append(change_to_calculate)  # the drastic change itself

            last_speed = current_speed
        avg = lambda l: float(sum(l)) / len(l) if len(l) > 0 else 0
        list_of_avg_for_each_list = lambda l: [avg(sublist) for sublist in l]

        avg_of_each_list_of_drastic_speed_change_per_minute = list_of_avg_for_each_list(l=list_of_lists_of_drastic_changes_per_minute)

        logging.debug('values per minute of: drastic speed change: ' + unicode(avg_of_each_list_of_drastic_speed_change_per_minute))

        avg_drastic_change = avg(avg_of_each_list_of_drastic_speed_change_per_minute)

        logging.debug('average per minute: ' + unicode(avg_drastic_change))

        return avg_drastic_change

    def __average_throttle_pressed_per_minitue(self, data):
        logging.debug('\n~ Average Throttle Presses Per Minute ~')

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

        logging.debug('values per minute of throttle presses: ' + unicode(list_of_presses_per_minute))
        # print list_of_presses_per_minute
        return float(sum(list_of_presses_per_minute)) / len(list_of_presses_per_minute)

    def __append_maximum_limitation_of_speed(self, data_unit):
        data_unit['maximum_limition_of_speed'] = self.speed_limit_client.get_maximum_limitation_of_speed_in_kmph(
            lat=data_unit['gps']['lat'],
            lon=data_unit['gps']['lon']
        )

    def get_good_driver_vectors(self):
        return [[0.5, 60, 0.2, 10, 0.15], [0.3, 30, 0.1, 8, 0.1]]

    def get_bad_driver_vectors(self):
        return [[0.6, 80, 0.35, 14, 0.23], [0.4, 45, 0.2, 12, 0.25]]