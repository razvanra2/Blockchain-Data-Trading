from seller import *
from buyer import *
class Data_transaction_monitor:
    def __init__(self, min_theta, seller_chain, new_buyer, data_seller):
        self.theta = min_theta
        self.chain = seller_chain
        self.buyer = new_buyer
        self.seller = data_seller

    def sale(self, buyer_deposit, i, money_i):
        if (buyer_deposit < self.theta):
            pass
        else:
            self.buyer.return_funds(buyer_deposit, money_i)
    
        target_block = self.chain.blocks[i]
        target_data = target_block.data

        decrypt_res, plain_block = self.buyer.decrypt_and_validate(target_data, i)

        if (decrypt_res is not False):
            self.buyer.extract_funds(buyer_deposit, money_i)
            self.seller.wire_funds(buyer_deposit, money_i)
            self.buyer.ensured_transfer(plain_block)
        else:
            if (self.arbitrate(plain_block, i) is True):
                self.buyer.extract_funds(buyer_deposit, money_i)
                self.seller.wire_funds(buyer_deposit, money_i)
            else:
                self.buyer.return_funds(buyer_deposit, money_i)

    # ARBITRATE (simplified)
    def arbitrate(self, plain_block, i):
        if self.chain.verify() and self.seller.validate(plain_block):
            return plain_block
        return None
