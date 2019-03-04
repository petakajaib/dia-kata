import numpy as np
from .entity_position_vector import get_entity_position_vector

def get_relative_entity_position_vector(entry, enriched_collection):
    entity_position = get_entity_position_vector(entry, enriched_collection)

    sorted_map = {}
    for idx, elem in enumerate(sorted(set(entity_position))):
        sorted_map[elem] = idx

    arr_relative = []
    for elem in entity_position:
        relative = sorted_map[elem]
        if relative == 0:
            arr_relative.append(1)
        else:
            arr_relative.append(1/relative)

    return np.array(arr_relative)
