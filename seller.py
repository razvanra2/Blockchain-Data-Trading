from math import ceil
import base64
import os
from blockchain import MinimalBlock, MinimalChain
from random import randint
from Crypto.Cipher import AES
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

backend = default_backend()


# SEGMENTING

def split_bytes_in_blocks(x, blocksize):
    nb_blocks = ceil(len(x)/blocksize)
    return [x[blocksize*i:blocksize*(i+1)] for i in range(nb_blocks)]


def pkcs7_padding(message, block_size):
    padding_length = block_size - (len(message) % block_size)
    if padding_length == 0:
        padding_length = block_size
    padding = bytes([padding_length]) * padding_length
    return message + padding


def pkcs7_strip(data):
    padding_length = data[-1]
    return data[:- padding_length]


def encrypt_aes_128_ecb(msg, key):
    padded_msg = pkcs7_padding(msg, block_size=16)
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
    encryptor = cipher.encryptor()
    return encryptor.update(padded_msg) + encryptor.finalize()


def decrypt_aes_128_ecb(ctxt, key):
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(ctxt) + decryptor.finalize()
    message = pkcs7_strip(decrypted_data)
    return message


def block_decrypt_aes_128_ecb(ctxt, i, key):
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(ctxt) + decryptor.finalize()
    message = pkcs7_strip(decrypted_data)
    return message[i * 16 : (i + 1) * 16]

cipher_text = ''


class Seller:
    def __init__(self):
        self.key = 'Mambo NumberFive'.encode()
        self.prefix = 'PREF'.encode()
        self.target = base64.b64decode(
            "Q2xhcCB5b3VyIGhhbmQgb25jZSBhbmQgY2xhcCB5b3VyIGhhbmRzIHR3aWNlCkFuZCBpZiBpdCBsb29rcyBsaWtlIHRoaXMgdGhlbiB5b3UgZG9pbmcgaXQgcmlnaHQ="
        )
        self.p_message = ''
        self.funds = 0

    def encrypt(self, message):
        global cipher_text

        self.p_message = message
        cipher_text = encrypt_aes_128_ecb(
            self.prefix + message + self.target,
            self.key)
        return cipher_text 

    # PRODUCING

    def prepare_transaction_data(self, plaintext, chain):
        ciphertext = self.encrypt(plaintext)
        blocks_count = int(len(ciphertext) / 16)

        for i in range(blocks_count):
            chain.add_block(ciphertext[i * 16: (i + 1) * 16])

        return chain

    def validate(self, plain_substring):
        return plain_substring in (self.prefix + self.p_message + self.target)

    def wire_funds(self, deposit, block_funds):
        self.funds += (deposit + block_funds)


'''
seller = Seller()
encripted = seller.encrypt(b"test string")
decripted = decrypt_aes_128_ecb(encripted, 'Mambo NumberFive'.encode())
print(len(encripted))
print(encripted)
c = seller.prepare_transaction_data(b"test string", MinimalChain())

print(c.blocks[1].timestamp)
print(c.blocks[1].data)
print(c.blocks[1].hash)


print(c.get_chain_size())
print(c.verify())
'''
