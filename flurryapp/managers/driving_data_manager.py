from django.db import models
import math

SPEED_RANGE = 5


class DrivingDataManager(models.Manager):
    def __init__(self):
        super(DrivingDataManager, self).__init__()
        self.last_speed_interval_value = SPEED_RANGE

    def append_new_driving_data(self, driving_data):
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
        for data_unit_index, data_unit in enumerate(driving_data):
            self.__append_maximum_limition_of_speed(data_unit)
            self.__append_angular_change(driving_data, data_unit_index)
            self.__append_speed_intervals(driving_data, data_unit_index)

        for item in driving_data:
            print item

    def __append_maximum_limition_of_speed(self, data_unit):
        data_unit['maximum_limition_of_speed'] = 0

    def __append_angular_change(self, driving_data, data_unit_index):
        if data_unit_index is 0:
            driving_data[data_unit_index]['angular_change'] = 0
        else:
            previous_coordinates = driving_data[data_unit_index - 1]['gps']
            current_coordinates = driving_data[data_unit_index]['gps']
            sub_y = previous_coordinates['lon'] - current_coordinates['lon']
            sub_x = previous_coordinates['lat'] - current_coordinates['lat']
            if sub_y is not 0:
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


if __name__ == '__main__':
    m = DrivingDataManager()
    m.append_new_driving_data([
        {
            'time': 123,
            'speed': 3,
            'rpm': 123,
            'gps': {
                'lat': 123,
                'lon': 123
            }
        },
        {
            'time': 124,
            'speed': 5,
            'rpm': 133,
            'gps': {
                'lat': 124,
                'lon': 124
            }
        },
        {
            'time': 125,
            'speed': 8,
            'rpm': 143,
            'gps': {
                'lat': 125,
                'lon': 125
            }
        },
    ])
