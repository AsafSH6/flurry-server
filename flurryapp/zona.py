import django

django.setup()

from flurryapp.models import *
import numpy as np
from sklearn.preprocessing import MinMaxScaler


def f():
    Driver.objects.extract_features()


def s():
    mms = MinMaxScaler()
    arr = np.array([0., 1., 2.])
    print mms.fit_transform(arr.reshape(-1, 1)).reshape(len(arr))
    # print mms.fit_transform(arr)#.reshape(1, -1)

# s()

# print np.array([0, 1, 2]).reshape(1, -1np.array([0., 1., 2.]))

print map(lambda x: x, [1, 2, 3])