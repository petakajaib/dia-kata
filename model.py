import random
from random import choice, randint
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.utils.validation import column_or_1d
import xgboost as xgb
import numpy as np
import pickle
from settings import *

random.seed(1337)
np.random.seed(1337)



def evaluate_single_extraction(prediction, truth):

    correct = True
    atleast_one = False
    for pred, test in zip(prediction, truth):

        pred_is_one = pred == 1.0
        pred_is_zero = pred == 0.0

        test_is_one = test == 1.0
        test_is_zero = test == 0.0

        if pred_is_one and test_is_zero:
            correct = False

        if pred_is_one and test_is_one:
            atleast_one = True


    if correct and atleast_one:
        return 1
    else:
        return 0

def filter_candidates(x, y, sorting_column=1, n=10):

    index_map = {}
    for idx, x_row in enumerate(x):
        index_map[tuple(x_row)] = idx

    sorted_x_vec = []
    sorted_y_vec = []
    for key in sorted(index_map.keys(), key=lambda x: x[sorting_column], reverse=True):

        sorted_x_vec.append(x[index_map[key]])
        sorted_y_vec.append(y[index_map[key]])

    x_arr = np.array(sorted_x_vec[:n])
    y_arr = np.array(sorted_y_vec[:n])

    return x_arr, y_arr

vectorized_data = pickle.load(open(VECTORIZED_PATH, "rb"))

feature_vectors = vectorized_data["feature_vectors"]

x_train, x_test, y_train, y_test = train_test_split(feature_vectors, vectorized_data["target_vectors"], test_size=0.33, random_state=1337)

clf = xgb.XGBClassifier(max_depth=8, n_jobs=6, objective="binary:logistic", random_state=1337)

x_train_stacked = np.vstack(x_train)
y_train_stacked = np.vstack(y_train)

y_reshaped = column_or_1d(y_train_stacked)

print("x_train_stacked shape", x_train_stacked.shape)

clf.fit(x_train_stacked, y_reshaped)

predictions = []

for x_test_section, y_test_section in zip(x_test, y_test):

    # filtered_x_test_section, filtered_y_test_section = filter_candidates(x_test_section, y_test_section)
    #
    # y_prediction = clf.predict(filtered_x_test_section)
    # y_test_reshaped = filtered_y_test_section.reshape(filtered_y_test_section.shape[0])

    y_prediction = clf.predict(x_test_section)
    y_test_reshaped = y_test_section.reshape(y_test_section.shape[0])

    predictions.append(evaluate_single_extraction(y_prediction, y_test_reshaped))

print("accuracy:", sum(predictions)/len(predictions))
