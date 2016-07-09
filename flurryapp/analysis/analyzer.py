from __future__ import unicode_literals
import django
django.setup()
from flurryapp.models import Driver
import logging

from sklearn.naive_bayes import GaussianNB, BernoulliNB, MultinomialNB


class Analyzer(object):
    def __init__(self, dict_of_target_and_its_features_vectors):
        logging.debug('\n\n** ANALYSIS **\n')
        self.dict_of_target_and_its_features_vectors = dict_of_target_and_its_features_vectors
        self.training_data_set, self.training_targets = self.__get_training_data()
        self.algorithm = MultinomialNB()
        logging.debug('Using Gaussian Naive Bayes\n\n')
        self.__fit()
        logging.getLogger().addHandler(logging.StreamHandler())

    def __fit(self):
        logging.debug('~ Fitting ~')
        self.algorithm.fit(self.training_data_set, self.training_targets)

    def classify(self):
        logging.debug('\n** CLASSIFY DATA **\n')

        data_set, targets = self.__get_data()
        logging.debug('Number of data sets: {num_data_sets}'.format(num_data_sets=len(data_set)))

        predictions = self.algorithm.predict(data_set)

        for prediction, target in zip(predictions, targets):
            logging.debug('Target {target} classified as: {prediction}'.format(target=target,
                                                                               prediction=prediction))

        logging.debug('\n')

        for target in self.dict_of_target_and_its_features_vectors.keys():
            num_of_vectors = len(self.dict_of_target_and_its_features_vectors[target])

            f = lambda target_and_classification: target_and_classification[0] == target and target_and_classification[1] == 'Good'
            vectors_classified_as_good = filter(f, zip(targets, predictions))

            logging.debug(target + ' has ' + unicode(num_of_vectors) + ' vectors and classified as good ' + unicode(len(vectors_classified_as_good)) + ' times')

            percentage = (float(len(vectors_classified_as_good)) / num_of_vectors) * 100

            logging.debug('Target {target} classified as Good Driver {percentage} % of the time\n'.format(target=target,
                                                                                                          percentage=percentage))

    def __get_data(self):
        data_set, targets = list(), list()
        for target, features in self.dict_of_target_and_its_features_vectors.iteritems():
            data_set += features
            targets += [target] * len(features)

        return data_set, targets

    def __get_training_data(self):
        # good_driver = Driver.objects.get_good_driver_vectors()
        # bad_driver = Driver.objects.get_bad_driver_vectors()
        good_driver, bad_driver = Driver.objects.good_and_bad_driver_vectors()

        training_data_set = good_driver + bad_driver
        training_targets = ['Good'] * len(good_driver) + ['Bad'] * len(bad_driver)

        return training_data_set, training_targets


if __name__ == '__main__':
    Analyzer(Driver.objects.extract_features(debug=True)).classify()
