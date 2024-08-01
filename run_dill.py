from hackathon.models.store import Message, Queue
from localstack.state import pickle


def _save():
    from hackathon.models.store import sqs_stores as st

    message = Message("just a message")
    queue = Queue()
    queue.add_message(message)
    reg_store = st["000000000000"]['us-east-1']
    reg_store.attribute["demo-queue"] = queue
    with open('store.pickle', 'wb') as p:
        pickle.dump(st, p)


def _load():
    with open('store.pickle', 'rb') as p:
        obk = pickle.load(p)
        print(obk)


if __name__ == '__main__':
    # renaming hackathon.models would break the loading!
    _save()
    _load()
