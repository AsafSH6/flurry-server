import django
django.setup()

from flurryapp.models import *

Driver.objects.extract_features()

# from sklearn import datasets
# from sklearn.naive_bayes import GaussianNB

# iris = datasets.load_iris()

# gnb = GaussianNB()
# y_pred = gnb.fit(iris.data, iris.target).predict(iris.data)
# print("Number of mislabeled points out of a total %d points : %d" % (iris.data.shape[0],(iris.target != y_pred).sum()))

# print iris.data.shape
# print iris.target

# print [5] * 3

# d = Driver.objects.all()[1]
# for ride in d:
#     print ride[-1]

# print sum([])