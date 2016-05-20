from __future__ import unicode_literals
from django.db import models
import math

from flurryapp.utils.maximum_limitation_of_speed import MaximumLimitationOfSpeedAPIClient

SPEED_RANGE = 5


class DriverManager(models.Manager):
    def __init__(self):
        super(DriverManager, self).__init__()
        self.last_speed_interval_value = SPEED_RANGE
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
            self.__append_maximum_limition_of_speed(data_unit)
            # self.__append_angular_change(driving_data, data_unit_index)
            # self.__append_speed_intervals(driving_data, data_unit_index)

        # for item in driving_data:
        #     print item
        driver.driving_data.data.append(driving_data)
        driver.driving_data.save()

    def __append_maximum_limition_of_speed(self, data_unit):
        data_unit['maximum_limition_of_speed'] = self.speed_limit_client.get_maximum_limitation_of_speed_in_kmph(
            lat=data_unit['gps']['lat'],
            lon=data_unit['gps']['lon']
        )

    def __append_angular_change(self, driving_data, data_unit_index):
        if data_unit_index is 0:
            driving_data[data_unit_index]['angular_change'] = 0
        else:
            previous_coordinates = driving_data[data_unit_index - 1]['gps']
            current_coordinates = driving_data[data_unit_index]['gps']
            sub_y = previous_coordinates['lon'] - current_coordinates['lon']
            sub_x = previous_coordinates['lat'] - current_coordinates['lat']
            if sub_y != 0:
                dev = sub_x / sub_y
                driving_data[data_unit_index]['angular_change'] = math.tan(dev)
            else:
                driving_data[data_unit_index]['angular_change'] = 0

    def __append_speed_intervals(self, driving_data, data_unit_index):
        if data_unit_index is 0:
            driving_data[data_unit_index]['speed_intervals'] = 0
        else:
            current_speed = driving_data[data_unit_index]['speed']
            if self.last_speed_interval_value - SPEED_RANGE <= current_speed <= self.last_speed_interval_value + SPEED_RANGE:
                previous_speed_intervals = driving_data[data_unit_index - 1]['speed_intervals']
                driving_data[data_unit_index]['speed_intervals'] = previous_speed_intervals + 1
            else:
                driving_data[data_unit_index]['speed_intervals'] = 0
                self.last_speed_interval_value = current_speed


# if __name__ == '__main__':
#     m = DriverManager()
#     m.append_new_driving_data(33, [
#         {
#             'time': 123,
#             'speed': 3,
#             'rpm': 123,
#             'gps': {
#                 'lat': 31.891520,
#                 'lon': 34.921453
#             }
#         },
#         {
#             'time': 124,
#             'speed': 5,
#             'rpm': 133,
#             'gps': {
#                 'lat': 31.891520,
#                 'lon': 34.921453
#             }
#         },
#         {
#             'time': 125,
#             'speed': 8,
#             'rpm': 143,
#             'gps': {
#                 'lat': 31.910071,
#                 'lon': 34.883599
#             }
#         },
#     ])
