import numpy as np
from .frequency_of_entity_vector import get_frequency_of_entity_vector

def get_relative_frequency_ranking_vector(entry, enriched_collection):
    freq = get_frequency_of_entity_vector(entry, enriched_collection)

    sorted_map = {}
    for idx, elem in enumerate(sorted(set(freq))):
        sorted_map[elem] = idx

    arr_relative = []
    for elem in freq:
        relative = sorted_map[elem]
        if relative == 0:
            arr_relative.append(1)
        else:
            arr_relative.append(1/relative)

    return np.array(arr_relative)
