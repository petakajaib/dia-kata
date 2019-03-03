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

def get_max_vals(feature_vectors):
    feature_vectors_stacked = np.vstack(feature_vectors)

    max_vals = []

    for i in range(feature_vectors_stacked.shape[1]):

        col = feature_vectors_stacked[:,i]
        max_val = np.max(col)

        max_vals.append(max_val)

    return max_vals

def normalize_feature_vectors(feature_vectors, index=None):

    max_vals = get_max_vals(feature_vectors)
    normalized_feature_vectors = []

    if index is None:
        columns_to_normalize_iterator = range(feature_vectors[0].shape[1])
    elif type(index) is list:
        columns_to_normalize_iterator = index


    for feature_vector in feature_vectors:

        normalized_feature_vector = []

        for i in columns_to_normalize_iterator:

            normalized_row = feature_vector[:,i]/max_vals[i]

            normalized_feature_vector.append(normalized_row.reshape(normalized_row.shape[0],1))

        normalized_feature_vectors.append(np.hstack(normalized_feature_vector))

    return normalized_feature_vectors

def balance_dataset(feature, target):

    if len(target[target == 0]) < len(target[target==1]):
        minority_class = 0
    else:
        minority_class = 1

    minority_marked = target == minority_class

    minority_class_data = []
    majority_class_data = []

    for idx, vec in enumerate(feature):

        if minority_marked[idx][0]:
            minority_class_data.append(vec)
        else:
            majority_class_data.append(vec)

    while len(minority_class_data) != len(majority_class_data):

        sampled_column = choice(minority_class_data)

        normal_noise = np.random.normal(scale=0.0001, size=sampled_column.shape)

        noise_added = normal_noise + sampled_column
        noise_added[noise_added < 0] = 0.0

        minority_class_data.append(noise_added)

    data_length = len(minority_class_data)

    if minority_class == 0:
        minority_target = np.zeros(data_length)
        majority_target = np.ones(data_length)
    elif minority_class == 1:
        minority_target = np.ones(data_length)
        majority_target = np.zeros(data_length)


    balanced_feature = np.vstack([np.vstack(minority_class_data), np.vstack(majority_class_data)])

    balanced_target = np.hstack([minority_target, majority_target])

    return balanced_feature, balanced_target

def downsample_dataset(feature, target):

    if len(target[target == 0]) < len(target[target==1]):
        minority_class = 0
    else:
        minority_class = 1

    minority_marked = target == minority_class

    minority_class_data = []
    majority_class_data = []

    for idx, vec in enumerate(feature):

        if minority_marked[idx][0]:
            minority_class_data.append(vec)
        else:
            majority_class_data.append(vec)

    while len(minority_class_data) != len(majority_class_data):

        random_index = randint(0, len(majority_class_data)-1)

        del(majority_class_data[random_index])

    data_length = len(minority_class_data)

    if minority_class == 0:
        minority_target = np.zeros(data_length)
        majority_target = np.ones(data_length)
    elif minority_class == 1:
        minority_target = np.ones(data_length)
        majority_target = np.zeros(data_length)


    balanced_feature = np.vstack([np.vstack(minority_class_data), np.vstack(majority_class_data)])

    balanced_target = np.hstack([minority_target, majority_target])

    return balanced_feature, balanced_target

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


    y_prediction = clf.predict(x_test_section)
    y_test_reshaped = y_test_section.reshape(y_test_section.shape[0])

    predictions.append(evaluate_single_extraction(y_prediction, y_test_reshaped))

print("accuracy:", sum(predictions)/len(predictions))
