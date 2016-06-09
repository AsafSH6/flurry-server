import django
django.setup()
from flurryapp.models import Driver

from sklearn.naive_bayes import GaussianNB, BernoulliNB, MultinomialNB
from sklearn import svm, tree


class Analyzer(object):
    def __init__(self, dict_of_target_and_its_features_vectors):
        self.data, self.target = self.__build_data_set(dict_of_target_and_its_features_vectors)
        # print '\n'.join(str(l) for l in self.data)
        # print '\n'.join(self.target)

    def learn(self, training_group_size_in_percentage=20):
        # slice_index = float(len(self.data)) / 100 * training_group_size_in_percentage
        f_data = self.data[:2] + self.data[5:8] + self.data[14:20]
        f_target = self.target[:2] + self.target[5:8] + self.target[14:20]
        p_data = self.data[2:5] + self.data[8:14] + self.data[20:]
        p_target = self.target[2:5] + self.target[8:14] + self.target[20:]

        print 'GAUSSIAN BN'
        gnb = GaussianNB()
        y_pred = gnb.fit(f_data, f_target).predict(p_data)

        print("Number of mislabeled points out of a total %d points : %d" % (len(p_data), (p_target != y_pred).sum()))
        print 'success:', 100 - (((p_target != y_pred).sum() / float(len(p_data))) * 100), '%'

        print '\n'

        print 'BERNOULLI BN'
        bnb = BernoulliNB()
        y_pred = bnb.fit(f_data, f_target).predict(p_data)

        print("Number of mislabeled points out of a total %d points : %d" % (len(p_data), (p_target != y_pred).sum()))
        print 'success:', 100 - (((p_target != y_pred).sum() / float(len(p_data))) * 100), '%'

        print '\n'

        print 'MULTINOMIAL NB'
        mnb = MultinomialNB()
        y_pred = mnb.fit(f_data, f_target).predict(p_data)

        print("Number of mislabeled points out of a total %d points : %d" % (len(p_data), (p_target != y_pred).sum()))
        print 'success:', 100 - (((p_target != y_pred).sum() / float(len(p_data))) * 100), '%'

        print '\n'

        print 'SVM'
        s = svm.SVC()
        s.fit(f_data, f_target)

        y_pred = s.predict(p_data)

        print("Number of mislabeled points out of a total %d points : %d" % (len(p_data), (p_target != y_pred).sum()))
        print 'success:', 100 - (((p_target != y_pred).sum() / float(len(p_data))) * 100), '%'

        print '\n'

        print 'DECISION TREE'
        t = tree.DecisionTreeClassifier()
        t = t.fit(f_data, f_target)

        y_pred = t.predict(p_data)

        print("Number of mislabeled points out of a total %d points : %d" % (len(p_data), (p_target != y_pred).sum()))
        print 'success:', 100 - (((p_target != y_pred).sum() / float(len(p_data))) * 100), '%'

        print '\n'



        # for i in xrange(len(y_pred)):
        #     print 'pred:', y_pred[i], 'real:', self.target[i], y_pred[i] == self.target[i]

    def __build_data_set(self, dict_of_target_and_its_features_vectors):
        data, targets = list(), list()
        for target, features_vectors in dict_of_target_and_its_features_vectors.iteritems():
            data += features_vectors
            targets += [target] * len(features_vectors)

        return data, targets





if __name__ == '__main__':
    Analyzer(Driver.objects.extract_features()).learn()