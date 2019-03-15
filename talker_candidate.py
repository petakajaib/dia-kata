
def get_talker_candidates(predictions_prob, entities, cluster_map, inverse_cluster_map, return_prob=False):

    predictions_set = set()

    entity_prob_map = {}

    for prediction_prob, entity in zip(predictions_prob,  entities):

        if prediction_prob[1] < 0.5:
            continue

        if cluster_map[entity] > -1:

            predictions_set = predictions_set.union(inverse_cluster_map[cluster_map[entity]])

            for ent in inverse_cluster_map[cluster_map[entity]]:
                entity_prob_map[ent] = prediction_prob
        else:
            predictions_set.add(entity)
            entity_prob_map[entity] = prediction_prob

    if return_prob:
        return [(p, entity_prob_map[p]) for p in predictions_set]
    else:
        return list(predictions_set)

def picking_from_talker_candidates():
    """
    Filter candidates based on following heuristics:

        - length between 4 - 30
        - no blacklisted characters:
            - 's
            - .
            - - (and other variations)
            - said
        - only take Person entities

    PageRank entities, pick top

    """
