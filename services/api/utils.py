from nacl.signing import VerifyKey
from nacl.encoding import HexEncoder
import binascii
import os


def verify_signature(signature, message):
    verify_key_hex = os.environ["VERIFY_KEY"]
    key_bytes = binascii.unhexlify(verify_key_hex)
    verify_key = VerifyKey(key_bytes)
    try:
        verify_key.verify(signature.encode(), encoder=HexEncoder)
        signature_body = binascii.unhexlify(signature)
        if signature_body[(-1*len(message)):].decode() != message:
            return False
    except Exception as e:
        print(str(e))
        return False
    return True
