import msgpack
from hackathon.models.store import Message, Queue

def get_store():
    from hackathon.models.store import sqs_stores as st

    message = Message("just a message")
    queue = Queue()
    queue.add_message(message)
    reg_store = st["000000000000"]['us-east-1']
    reg_store.attribute["demo-queue"] = queue
    return st


if __name__ == '__main__':
    structure = {"key": {
        "Name": "Value"
    }}

    packed = msgpack.packb(structure)
    unpacked = msgpack.unpackb(packed)
    assert unpacked == structure
    print(unpacked)

    _store = get_store()
    packed = msgpack.packb(_store)


