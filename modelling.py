from sklearn.model_selection import train_test_split
import xgboost as xgb
import numpy as np
import pickle
from settings import *

vectorized_data = pickle.load(open(VECTORIZED_PATH, "rb"))

x_train, x_test, y_train, y_test = train_test_split(vectorized_data["feature_vectors"], vectorized_data["target_vectors"], test_size=0.33, random_state=1337)


clf = xgb.XGBClassifier(max_depth=8, n_jobs=6, objective="binary:logistic")

x_train_stacked = np.vstack(x_train)
y_train_stacked = np.vstack(y_train)

clf.fit(x_train_stacked, y_train_stacked)


#
# y_prediction = clf.predict(x_test)
# acc = accuracy_score(y_prediction, y_test)
