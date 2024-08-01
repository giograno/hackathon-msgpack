from localstack.services.stores import AccountRegionBundle, LocalAttribute, BaseStore
import msgpack


class Message:
    content: str

    def __init__(self, content: str):
        self.content = content

    def to_msgpack(self):
        return msgpack.packb(self.content)

    @classmethod
    def from_msgpack(cls, data):
        content = msgpack.unpackb(data)
        return cls(content)

class Queue:
    messages: list[Message]

    def __init__(self):
        self.messages = []

    def add_message(self, message: Message):
        self.messages.append(message)

    def to_msgpack(self):
        from hackathon.msgpack import pickle
        messages_data = [pickle.dumps(message) for message in self.messages]
        return msgpack.packb(messages_data)

    @classmethod
    def from_msgpack(cls, data):
        from hackathon.msgpack import pickle
        messages_data = pickle.loads(data)
        queue = cls()
        for message_data in messages_data:
            message = pickle.loads(message_data)
            queue.add_message(message)
        return queue


class Store(BaseStore):
    attribute: [str, Queue] = LocalAttribute(dict)

    def to_msgpack(self):
        from hackathon.msgpack import pickle
        d = {}
        for att, value in self.attribute.items():
            d[att] = pickle.dumps(value)
        return msgpack.packb(d)

    @classmethod
    def from_msgpack(cls, data):
        from hackathon.msgpack import pickle
        attribute_dict = pickle.loads(data)
        store = cls()
        for k, v in attribute_dict.items():
            store.attribute[k] = pickle.loads(v)
        return store


sqs_stores = AccountRegionBundle("sqs", Store)
