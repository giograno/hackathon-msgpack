import msgpack

from hackathon.models.store import Message, Queue, Store

MESSAGE_TYPE = 3
QUEUE_TYPE = 4
STORE_TYPE = 5


def ext_type_serializer():

    def encoder(obj):
        if isinstance(obj, Message):
            return msgpack.ExtType(MESSAGE_TYPE, obj.to_msgpack())
        elif isinstance(obj, Queue):
            return msgpack.ExtType(QUEUE_TYPE, obj.to_msgpack())
        elif isinstance(obj, Store):
            return msgpack.ExtType(STORE_TYPE, obj.to_msgpack())
        return obj

    return encoder


def ext_type_deserializer(code, data):
    if code == MESSAGE_TYPE:
        return Message.from_msgpack(data)
    elif code == QUEUE_TYPE:
        return Queue.from_msgpack(data)
    elif code == STORE_TYPE:
        return Store.from_msgpack(data)
    return msgpack.ExtType(code, data)


def dumps(obj):
    return msgpack.packb(obj, default=ext_type_serializer())


def dump(obj, file):
    file.write(dumps(obj))


def load(file):
    return loads(file.read())


def loads(data):
    return msgpack.unpackb(data, ext_hook=ext_type_deserializer)
