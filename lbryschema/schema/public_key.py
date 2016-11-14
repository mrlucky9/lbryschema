from copy import deepcopy

from Crypto.Hash import SHA256
from lbryschema.schema import public_key_pb2
from lbryschema.schema.schema import Schema


class _RSAKeyHelper(object):
    def __init__(self, key):
        self._key = key

    @property
    def der(self):
        return self._key.publickey().exportKey('DER')

    @property
    def hash(self):
        return SHA256.new(self.der).digest()


class RSAPublicKey(Schema):
    @classmethod
    def load(cls, message):
        _key = deepcopy(message)
        public_key = _key.pop("public_key")
        public_key_hash = _key.pop("public_key_hash")
        _message_pb = public_key_pb2.RSAPublicKey()
        _message_pb.public_key = public_key
        _message_pb.public_key_hash = public_key_hash
        return cls._load(_key, _message_pb)

    @classmethod
    def load_from_key_obj(cls, key):
        _key = _RSAKeyHelper(key)
        msg = {
            "version": "_0_0_1",
            "public_key": _key.der,
            "public_key_hash": _key.hash
        }
        return cls.load(msg)


class RSASignature(Schema):
    @classmethod
    def load(cls, message):
        _signature = deepcopy(message)
        _message_pb = public_key_pb2.RSASignature()
        _message_pb.signature = _signature.pop("signature")
        _message_pb.public_key_hash = _signature.pop("public_key_hash")
        return cls._load(_signature, _message_pb)

    @classmethod
    def load_from_key_obj(cls, key, signature):
        _key = _RSAKeyHelper(key)
        msg = {
            "version": "_0_0_1",
            "signature": signature,
            "public_key_hash": _key.hash
        }
        return cls.load(msg)