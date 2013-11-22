from message_string_generator import MessageStringGenerator
from datum import Datum
from types import TInt, TFloat, TBool, TString, TRaw, TNullable, TList, TMap, TTuple, TUserDef, TObject
from client import Client, ClientBase, TypeMismatch, UnknownMethod

from contextlib import contextmanager

@contextmanager
def connect(cls, host, port, name, timeout=10):
    client = cls(host, port, name, timeout)
    try:
        yield(client)
    finally:
        client.get_client().close()
