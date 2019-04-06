from redis import StrictRedis


def populate_sub():

    try:
        parsed = Text(article["content"])
        entities = [" ".join(entity).lower() for entity in parsed.entities]

        entity = {
            "entities": entities,
            "url": article["url"],
            "detected_language": parsed.detect_language(),
            "publish_date": article["publish_date"]
        }

        entity_collection.insert_one(entity)

    except pycld2.error as err:
        print(err)
    except ValueError as err:
        print(err)
        continue

redis_client = StrictRedis()
redis_pubsub = redis_client.pubsub()

redis_pubsub.subscribe('populate_entities')

while True:

    message = p.get_message()                                               # Checks for message
    if message:
        data = message['data']

        parsed = json.loads(data)
        print(parsed)
