from __future__ import unicode_literals
import requests as req


API_APP_ID = 'CYfTUgmUWqfylJcctLRO'
API_APP_CODE = 'MW3akKCzl263Qtt7qHgIUQ'


MAX_SPEED_API_URL = r'http://route.st.nlp.nokia.com/routing/6.2/getlinkinfo.json?' \
                    r'waypoint={{gps_lat}},{{gps_lon}}' \
                    r'&app_id={app_id}' \
                    r'&app_code={app_code}'.format(app_id=API_APP_ID, app_code=API_APP_CODE)

MS_TO_KMPH_FACTOR = 3.6


class MaximumLimitationOfSpeedAPIClient(object):
    def __init__(self):
        pass

    def get_maximum_limitation_of_speed_in_kmph(self, lat, lon):
        response = req.get(MAX_SPEED_API_URL.format(gps_lat=lat, gps_lon=lon))
        maximum_speed_limit_in_kmph = self.__get_maximum_speed_in_kmph_from_response(response=response)
        return maximum_speed_limit_in_kmph

    def __get_maximum_speed_in_kmph_from_response(self, response):
        if response.status_code != 200:
            return -1
        response_json = response.json()['Response']
        speed_details = response_json['Link'][0]
        if 'SpeedLimit' in speed_details:
            maximum_speed = speed_details['SpeedLimit']
        elif 'BaseSpeed' in speed_details['DynamicSpeedInfo']:
            maximum_speed = speed_details['DynamicSpeedInfo']['BaseSpeed']
        else:
            return -1
        return self.__convert_speed_to_kmph(speed=maximum_speed)

    def __convert_speed_to_kmph(self, speed):
        return round(speed * MS_TO_KMPH_FACTOR)

if __name__ == '__main__':
    client = MaximumLimitationOfSpeedAPIClient()
    print client.get_maximum_limitation_of_speed_in_kmph(31.891520, 34.921453)
    print client.get_maximum_limitation_of_speed_in_kmph(31.910071, 34.883599)
    print client.get_maximum_limitation_of_speed_in_kmph(32.036529, 34.843201)