from sklearn.model_selection import train_test_split
from sklearn.utils.validation import column_or_1d
import xgboost as xgb
import numpy as np
import pickle
from settings import *


def modelling(vectorized_path):

    vectorized_data = pickle.load(open(vectorized_path, "rb"))

    feature_vectors = vectorized_data["feature_vectors"]

    feature_vectors_stacked = np.vstack(feature_vectors)

    max_vals = []

    for i in range(feature_vectors_stacked.shape[1]):

        col = feature_vectors_stacked[:,i]
        max_val = np.max(col)

        max_vals.append(max_val)

    normalized_feature_vectors = []

    for feature_vector in feature_vectors:

        normalized_feature_vector = []

        for i in range(feature_vector.shape[1]):

            normalized_row = feature_vector[:,i]/max_vals[i]

            normalized_feature_vector.append(normalized_row.reshape(normalized_row.shape[0],1))

        normalized_feature_vectors.append(np.hstack(normalized_feature_vector))

    x_train, x_test, y_train, y_test = train_test_split(normalized_feature_vectors, vectorized_data["target_vectors"], test_size=0.33, random_state=1337)


    clf = xgb.XGBClassifier(max_depth=8, n_jobs=6, objective="binary:logistic", random_state=1337)

    x_train_stacked = np.vstack(x_train)
    y_train_stacked = np.vstack(y_train)

    y_reshaped = column_or_1d(y_train_stacked)

    clf.fit(x_train_stacked, y_reshaped)

    for x_test_section, y_test_section in zip(x_test, y_test):

        y_prediction_proba = clf.predict_proba(x_test_section)
        y_prediction = clf.predict(x_test_section)
        y_test_reshaped = y_test_section.reshape(y_test_section.shape[0])

        print("truth\t", y_test_reshaped)
        print("prediction\t", y_prediction)
        print("predict_proba\t",y_prediction_proba)
