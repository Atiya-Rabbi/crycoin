import hashlib
import json
from datetime import datetime


class Block(object):
    # RIGHT_ANS = 'cry'
    RIGHT_ANS = '1'
    
    def __init__(self, transaction_list, index, time=datetime.now().strftime("%m/%d/%Y, %H:%M:%S")):
        self.primary_ky = index
        self.prev_blk_hash = ''
        self.time = time
        self.blk_data = transaction_list
        self.nonce = 0
        self.curr_blk_hash = self.generate_hash()

    def generate_hash(self):
        complete_trans_hash = ''
        print('------------->',self.blk_data)
        for hash in self.blk_data:
            complete_trans_hash += hash.hash
        
        hash_it = (str(self.nonce) + self.prev_blk_hash + str(self.time) + str(self.primary_ky) + complete_trans_hash).encode()
        print('hash_it==>', hash_it)

        return hashlib.sha256(hash_it).hexdigest()

    def mining_the_block(self):
        while self.curr_blk_hash[0:len(self.RIGHT_ANS)] != self.RIGHT_ANS:
            self.nonce += 1
            self.curr_blk_hash = self.generate_hash()

        print('FOUND--------->',self.curr_blk_hash)
        print('NONCE--------->',self.nonce)


class Balance(object):
    def __init__(self):
        self.current_balance = 100

    def add_balance(self):
        self.current_balance = self.current_balance + 50