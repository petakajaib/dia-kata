import random
import json
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

def evaluate_model(x_test, y_test, model):
    predictions = []

    for x_test_section, y_test_section in zip(x_test, y_test):

        reshaped = column_or_1d(y_test_section)

        if sum(reshaped) == 0:
            continue

        y_prediction = clf.predict(x_test_section)
        y_test_reshaped = y_test_section.reshape(y_test_section.shape[0])

        predictions.append(evaluate_single_extraction(y_prediction, y_test_reshaped))

    acc = sum(predictions)/len(predictions)
    print("accuracy:", acc)
    return acc

if __name__ == '__main__':

    vectorized_data = pickle.load(open(VECTORIZED_PATH, "rb"))

    feature_vectors = vectorized_data["feature_vectors"]

    x_train, x_test, y_train, y_test = train_test_split(feature_vectors, vectorized_data["target_vectors"], test_size=0.33, random_state=1337)


    clf = xgb.XGBClassifier(max_depth=8, n_jobs=6, objective="binary:logistic", random_state=1337)

    x_train_stacked = np.vstack(x_train)
    y_train_stacked = np.vstack(y_train)

    y_reshaped = column_or_1d(y_train_stacked)

    print("x_train_stacked shape", x_train_stacked.shape)

    clf.fit(x_train_stacked, y_reshaped)
    evaluate_model(x_test, y_test, clf)

    pickle.dump(clf, open(CURRENT_BEST_MODEL, "wb"))
