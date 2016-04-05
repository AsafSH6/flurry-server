import numpy as np
from sklearn import preprocessing
import django
django.setup()
from flurryapp.models import Driver, Profile


class Analyzer(object):
    def __init__(self, data_json):
        self.data = self.__extract_relevant_data(data_json)
        # print self.data

    def analyze_data(self):
        self.__preprocess()
        print self.data

    def __extract_relevant_data(self, rides_data):
        keys = rides_data[0].keys()
        data = list()
        for ride in rides_data:
            # iter over rows in ride till the last row (when the last row is the maximum between all feature data rows)
            for row_index in xrange(max([len(ride[key]) for key in keys])):
                data.append(list())
                # iter over each key (speed, rpm etc...) and add to the last list the values in the ride
                for key in keys:
                    data[-1].append(ride[key][row_index]['value'] if row_index < len(ride[key]) else 0)

        return np.array(data)

    def __preprocess(self):
        self.data = preprocessing.MinMaxScaler(feature_range=(0, 1)).fit_transform(self.data)


if __name__ == '__main__':
    Analyzer(Profile.objects.create_new_profile_for_driver(Driver.objects.get(id=7))).analyze_data()