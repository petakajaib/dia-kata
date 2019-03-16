
def get_talker_candidates(predictions_prob, entities, cluster_map, inverse_cluster_map, return_prob=False):

    predictions_set = set()

    entity_prob_map = {}

    for prediction_prob, entity in zip(predictions_prob,  entities):

        if prediction_prob[1] < 0.5:
            continue

        if cluster_map[entity] != -1:

            predictions_set = predictions_set.union(inverse_cluster_map[cluster_map[entity]])
            if return_prob:
                for ent in inverse_cluster_map[cluster_map[entity]]:
                    entity_prob_map[ent] = prediction_prob
        else:
            predictions_set.add(entity)

    if return_prob:
        for prediction_prob, entity in zip(predictions_prob,  entities):

            if prediction_prob[1] < 0.5:
                continue

            if cluster_map[entity] == -1:
                entity_prob_map[entity] = prediction_prob

    if return_prob:
        return [(p, entity_prob_map[p]) for p in predictions_set]
    else:
        return list(predictions_set)

def filter_candidates_by_heuristics(entities, entity_tags):
    """
    Filter candidates based on following heuristics:

        - length between 4 - 30
        - no blacklisted characters:
            - 's
            - .
            - - (and other variations)
            - said
        - only take Person entities
    """
    filtered_entity = []
    hyphens = [
        "‐",
        "‑",
        "‒",
        "–",
        "—",
        "―"
    ]
    for entity in entities:
        char_length = len(entity)
        if char_length < 4 or char_length > 25:
            continue

        if "'s" in entity.lower():
            continue

        if "." in entity.lower():
            continue

        has_hyphen = False
        for hyphen in hyphens:
            if hyphen in entity:
                has_hyphen = True
        if has_hyphen:
            continue

        if "said" in entity.lower():
            continue

        if entity_tags[entity.lower()] != "I-PER":
            continue

        filtered_entity.append(entity)

    return filtered_entity

def select_candidate(talker_candidates, entity_tags):

    filtered_condidates = filter_candidates_by_heuristics(talker_candidates, entity_tags)
    if filtered_condidates:
        return max(filtered_condidates, key=lambda x: len(x))
