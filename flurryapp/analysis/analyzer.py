import django
django.setup()
from flurryapp.models import Driver

from sklearn.naive_bayes import GaussianNB, BernoulliNB, MultinomialNB
from sklearn import svm, tree
from sklearn.ensemble import AdaBoostClassifier


class Analyzer(object):
    def __init__(self, dict_of_target_and_its_features_vectors, training_group_size_in_percentage=40):
        self.dict_of_target_and_its_features_vectors = dict_of_target_and_its_features_vectors
        self.training_data_sets, self.training_targets,\
        self.testing_data_sets, self.test_targets = self.__get_training_group_and_testing_group(training_group_size_in_percentage)
        print self.training_targets

        print 'num of training sets:', len(self.training_targets)
        print 'num of testing sets:', len(self.test_targets)
        print 'number of valid rides', sum(len(driver) for driver in Driver.objects.all() if len(driver) > 1 and driver.name != 'Test Driver')

    def learn1(self):
        # slice_index = float(len(self.data)) / 100 * training_group_size_in_percentage

        print 'GAUSSIAN BN'
        gnb = GaussianNB()
        y_pred = gnb.fit(self.training_data_sets, self.training_targets).predict(self.testing_data_sets)

        print("Number of mislabeled points out of a total %d points : %d" % (len(self.testing_data_sets), (self.test_targets != y_pred).sum()))
        print 'success:', 100 - (((self.test_targets != y_pred).sum() / float(len(self.testing_data_sets))) * 100), '%'

        print '\n'

        print 'BERNOULLI BN'
        bnb = BernoulliNB()
        y_pred = bnb.fit(self.training_data_sets, self.training_targets).predict(self.testing_data_sets)

        print("Number of mislabeled points out of a total %d points : %d" % (len(self.testing_data_sets), (self.test_targets != y_pred).sum()))
        print 'success:', 100 - (((self.test_targets != y_pred).sum() / float(len(self.testing_data_sets))) * 100), '%'

        print '\n'

        print 'MULTINOMIAL NB'
        mnb = MultinomialNB()
        y_pred = mnb.fit(self.training_data_sets, self.training_targets).predict(self.testing_data_sets)

        print("Number of mislabeled points out of a total %d points : %d" % (len(self.testing_data_sets), (self.test_targets != y_pred).sum()))
        print 'success:', 100 - (((self.test_targets != y_pred).sum() / float(len(self.testing_data_sets))) * 100), '%'

        print '\n'

        print 'SVM'
        s = svm.SVC()
        s.fit(self.training_data_sets, self.training_targets)

        y_pred = s.predict(self.testing_data_sets)

        print("Number of mislabeled points out of a total %d points : %d" % (len(self.testing_data_sets), (self.test_targets != y_pred).sum()))
        print 'success:', 100 - (((self.test_targets != y_pred).sum() / float(len(self.testing_data_sets))) * 100), '%'

        print '\n'

        print 'DECISION TREE'
        t = tree.DecisionTreeClassifier(max_depth=2)
        t = t.fit(self.training_data_sets, self.training_targets)

        y_pred = t.predict(self.testing_data_sets)

        print("Number of mislabeled points out of a total %d points : %d" % (len(self.testing_data_sets), (self.test_targets != y_pred).sum()))
        print 'success:', 100 - (((self.test_targets != y_pred).sum() / float(len(self.testing_data_sets))) * 100), '%'

        print '\n'

        print 'REAL ADA BOOST'
        bdt_real = AdaBoostClassifier(
            tree.DecisionTreeClassifier(max_depth=2),
            n_estimators=600,
            learning_rate=1)
        bdt_real = bdt_real.fit(self.training_data_sets, self.training_targets)

        y_pred = bdt_real.predict(self.testing_data_sets)

        print("Number of mislabeled points out of a total %d points : %d" % (
        len(self.testing_data_sets), (self.test_targets != y_pred).sum()))
        print 'success:', 100 - (((self.test_targets != y_pred).sum() / float(len(self.testing_data_sets))) * 100), '%'

        print '\n'

        print 'DISCERT ADA BOOST'
        bdt_discrete = AdaBoostClassifier(
                    tree.DecisionTreeClassifier(max_depth=2),
                    n_estimators=600,
                    learning_rate=1.5,
                    algorithm="SAMME")
        bdt_discrete = bdt_discrete.fit(self.training_data_sets, self.training_targets)

        y_pred = bdt_discrete.predict(self.testing_data_sets)

        print("Number of mislabeled points out of a total %d points : %d" % (
            len(self.testing_data_sets), (self.test_targets != y_pred).sum()))
        print 'success:', 100 - (((self.test_targets != y_pred).sum() / float(len(self.testing_data_sets))) * 100), '%'

        print '\n'


        # for i in xrange(len(y_pred)):
        #     print 'pred:', y_pred[i], 'real:', self.target[i], y_pred[i] == self.target[i]

    def learn(self):
        pass


    def __build_data_set(self):
        data, targets = list(), list()
        for target, features_vectors in self.dict_of_target_and_its_features_vectors.iteritems():
            data += features_vectors
            targets += [target] * len(features_vectors)

        return data, targets

    def __get_training_group_and_testing_group(self, training_group_size_in_percentage):
        training_data_set, training_targets = list(), list()
        testing_data_set, testing_targets = list(), list()
        for target, features_vector in self.dict_of_target_and_its_features_vectors.iteritems():
            number_of_vectors = len(features_vector)
            slice_index = int(float(number_of_vectors) * (float(training_group_size_in_percentage) / 100))
            training_data_set += features_vector[:slice_index]
            training_targets += [target] * slice_index

            testing_data_set += features_vector[slice_index:]
            testing_targets += [target] * (number_of_vectors - slice_index)

        return training_data_set, training_targets, testing_data_set, testing_targets








if __name__ == '__main__':
    Analyzer(Driver.objects.extract_features()).learn1()
    # pchange_to_calculaterint Analyzer(Driver.objects.extract_features()).learn()