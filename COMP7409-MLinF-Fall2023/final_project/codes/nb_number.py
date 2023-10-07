from collections import Counter

import numpy as np
from numpy import ndarray, exp, pi, sqrt
from Readdata import Readdata
from Evaluation import Evaluation



class nb_number:

    def __init__(self):
        self.nclass = None # class number
        self.prior = None # priori probability
        self.avgs = None # mean
        self.vars = None # variance


    def _get_avgs(self, data: ndarray, label: ndarray) -> ndarray:
        # Calculate means of training data.

        return np.array([data[label == i].mean(axis=0) for i in range(self.nclass)])

    def _get_vars(self, data: ndarray, label: ndarray) -> ndarray:
        # Calculate variances of training data.

        return np.array([data[label == i].var(axis=0) for i in range(self.nclass)])

    def _get_prior(self, label: ndarray) -> ndarray:
        # Calculate prior probability.



        cnt = Counter(label)
        prior = np.array([cnt[i] / len(label) for i in range(len(cnt))])
        return prior



    def _get_con_prob(self, row: ndarray) -> ndarray:
        # calculate the conditional probability


        return (1 / sqrt(2 * pi * self.vars) * exp(
            -(row - self.avgs)**2 / (2 * self.vars))).prod(axis=1)

    def fit(self, data: ndarray, label: ndarray):
        # Build a Gauss naive bayes classifier.

        # Calculate prior probability.
        self.prior = self._get_prior(label)
        # Count number of classes.
        self.nclass = len(self.prior)
        # Calculate the mean.
        self.avgs = self._get_avgs(data, label)
        # Calculate the variance.
        self.vars = self._get_vars(data, label)

    def predict_prob(self, data: ndarray) -> ndarray:
        # Get the probability of label.

        # Calculate the joint probabilities of each feature and each class.
        likelihood = np.apply_along_axis(self._get_con_prob, axis=1, arr=data)
        probs = self.prior * likelihood
        # Scale the probabilities to for further method
        probs_sum = probs.sum(axis=1)
        return probs / probs_sum[:, None]

    def predict(self, data: ndarray) -> ndarray:
        # Get the prediction of label.

        # Choose the class which has the maximum probability
        return self.predict_prob(data).argmax(axis=1)


# Import data from Readdata
realdata = Readdata.train_data
reallabel = Readdata.train_label
realtestdata = Readdata.test_data
realtestlabel = Readdata.test_label

reallabel = np.array(reallabel)
realdata = np.array(realdata)
realtestlabel = np.array(realtestlabel)
realtestdata = np.array(realtestdata)
reallabel = reallabel.astype(float)
realdata = realdata.astype(float)
realtestdata = realtestdata.astype(float)
realtestlabel = realtestlabel.astype(int)

# Train and test using my Naive Bayes
clf = nb_number()
clf.fit(realdata, reallabel)
y_hat = clf.predict(realtestdata)

eva=Evaluation()
acc=eva.accuracy(realtestlabel, y_hat)
pre=eva.precision(realtestlabel, y_hat)
rec=eva.recall(realtestlabel, y_hat)
F1=eva.F1(realtestlabel, y_hat)

# Evaluate the result
print("Accuracy:", acc)
print("Precision:",pre)
print("Recall:",rec)
print("F1:",F1)
eva.ConfusionMatrix(realtestlabel, y_hat,len(np.unique(y_hat)))

