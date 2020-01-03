import random
from seller import *

class Buyer:
    def __init__(self, seller_key):
        self.key = seller_key
        self.funds = 1200
        self.text = None

    def return_funds(self, deposit, expenses):
        self.funds += (deposit + expenses)

    def extract_funds(self, deposit, expenses):
        self.funds -= (deposit + expenses)

    def decrypt_and_validate(self, target_data, i):
        plain = block_decrypt_aes_128_ecb(target_data, i, self.key)

        if random.randint(0,1) % 2 == 0:
            self.text += plain
            return True, plain
        return False, plain
    
    def ensured_transfer(self, plain_block):
        if (self.text is None):
            self.text = plain_block
        else:
            self.text = plain_block