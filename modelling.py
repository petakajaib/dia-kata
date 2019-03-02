from sklearn.model_selection import train_test_split
from sklearn.utils.validation import column_or_1d
import xgboost as xgb
import numpy as np
import pickle
from settings import *


vectorized_data = pickle.load(open(VECTORIZED_PATH, "rb"))


feature_vectors = vectorized_data["feature_vectors"]

feature_vectors_stacked = np.vstack(feature_vectors)

feature_vectors_stacked_normalized = []

for i in range(feature_vectors_stacked.shape[1]):

    col = feature_vectors_stacked[:,i]
    max_val = np.max(col)

    col_normalized = col/max_val
    feature_vectors_stacked_normalized.append(col_normalized.reshaped(col_normalized.shape[0],1))

feature_vectors_stacked_normalized = np.hstack(feature_vectors_stacked_normalized)

x_train, x_test, y_train, y_test = train_test_split(feature_vectors_stacked_normalized, vectorized_data["target_vectors"], test_size=0.33, random_state=1337)


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
