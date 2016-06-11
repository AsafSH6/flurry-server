import django
from sklearn.ensemble import AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB, BernoulliNB, MultinomialNB

django.setup()

from flurryapp.models import *
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from sklearn import tree, svm


def f():
    features = Driver.objects.extract_features()
    # good = Driver.objects.get_good_driver_vectors()
    # bad = Driver.objects.get_bad_driver_vectors()
    #
    # test = good + bad
    # target = ['good'] * len(good) + ['bad'] * len(bad)
    #
    #
    # print 'GAUSSIAN BN'
    # gnb = GaussianNB()
    # y_pred = gnb.fit(test, target).predict(features['Asaf Shavit'])
    #
    # print 'good:', len(filter(lambda x: x == 'good', y_pred))
    # print 'bad:', len(filter(lambda x: x == 'bad', y_pred))
    #
    # print '\n'
    #
    # print 'BERNOULLI BN'
    # bnb = BernoulliNB()
    # y_pred = bnb.fit(test, target).predict(features['Asaf Shavit'])
    #
    # print 'good:', len(filter(lambda x: x == 'good', y_pred))
    # print 'bad:', len(filter(lambda x: x == 'bad', y_pred))
    #
    # print '\n'
    #
    # print 'MULTINOMIAL NB'
    # mnb = MultinomialNB()
    # y_pred = mnb.fit(test, target).predict(features['Asaf Shavit'])
    #
    # print 'good:', len(filter(lambda x: x == 'good', y_pred))
    # print 'bad:', len(filter(lambda x: x == 'bad', y_pred))
    #
    # print '\n'
    #
    # print 'SVM'
    # s = svm.SVC()
    # s.fit(test, target)
    #
    # y_pred = s.predict(features['Asaf Shavit'])
    #
    # print 'good:', len(filter(lambda x: x == 'good', y_pred))
    # print 'bad:', len(filter(lambda x: x == 'bad', y_pred))
    #
    # print '\n'
    #
    # print 'DECISION TREE'
    # t = tree.DecisionTreeClassifier(max_depth=2)
    # t = t.fit(test, target)
    #
    # y_pred = t.predict(features['Asaf Shavit'])
    #
    # print 'good:', len(filter(lambda x: x == 'good', y_pred))
    # print 'bad:', len(filter(lambda x: x == 'bad', y_pred))
    #
    # print '\n'
    #
    # print 'REAL ADA BOOST'
    # bdt_real = AdaBoostClassifier(
    #     tree.DecisionTreeClassifier(max_depth=2),
    #     n_estimators=600,
    #     learning_rate=1)
    # bdt_real = bdt_real.fit(test, target)
    #
    # y_pred = bdt_real.predict(features['Asaf Shavit'])
    #
    # print 'good:', len(filter(lambda x: x == 'good', y_pred))
    # print 'bad:', len(filter(lambda x: x == 'bad', y_pred))
    #
    # print '\n'
    #
    # print 'DISCERT ADA BOOST'
    # bdt_discrete = AdaBoostClassifier(
    #     tree.DecisionTreeClassifier(max_depth=2),
    #     n_estimators=600,
    #     learning_rate=1.5,
    #     algorithm="SAMME")
    # bdt_discrete = bdt_discrete.fit(test, target)
    #
    # y_pred = bdt_discrete.predict(features['Asaf Shavit'])
    #
    # print 'good:', len(filter(lambda x: x == 'good', y_pred))
    # print 'bad:', len(filter(lambda x: x == 'bad', y_pred))
    #
    # print '\n'

f()

def s():
    mms = MinMaxScaler()
    arr = np.array([0., 1., 2.])
    print mms.fit_transform(arr.reshape(-1, 1)).reshape(len(arr))
    # print mms.fit_transform(arr)#.reshape(1, -1)

# s()

# print np.array([0, 1, 2]).reshape(1, -1np.array([0., 1., 2.]))

# print map(lambda x: x, [1, 2, 3])