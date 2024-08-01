from hackathon.models.store import Message, Queue


def get_store():
    from hackathon.models.store import sqs_stores as st

    message = Message("just a message")
    queue = Queue()
    queue.add_message(message)
    reg_store = st["000000000000"]['us-east-1']
    reg_store.attribute["demo-queue"] = queue
    return st


def _save():
    from hackathon.msgpack import pickle
    _store = get_store()
    with open('store.msg', 'wb') as p:
        pickle.dump(_store, p)


def _load():
    from hackathon.msgpack import pickle
    with open('store.msg', 'rb') as p:
        restored = pickle.load(p)

    print(restored)


if __name__ == '__main__':
    _save()
    _load()

# Pros
# - more resilient to class changes
# - we can control better what goes into store
#   - it crashes if we don't define an Ext class
# - we can gradually roll the migration with a fallback to pickle
# - language agnostic when we'll rewrite LocalStack in Rust!
# https://shopify.engineering/caching-without-marshal-part-two-messagepack
