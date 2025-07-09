from tronpy import Tron
from tronpy.keys import PrivateKey

client = Tron()


def create_wallet():
    priv_key = PrivateKey.random()
    address = priv_key.public_key.to_base58check_address()
    return address, priv_key.hex()
