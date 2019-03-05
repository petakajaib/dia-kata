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
