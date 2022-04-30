from datetime import datetime
import hashlib
import json
try:
    from crycoin.views.user_block import UserBlock
except:
    from views.user_block import UserBlock


class Transaction(object):
    def __init__(self, sender, receiver, amt):
        self.sender = sender
        self.receiver = receiver
        self.amount = amt
        self.time_stamp = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        self.signature = False
        self.hash = self.generate_hash()

    def generate_hash(self):
        hash_it = (self.sender + str(self.amount) + str(self.time_stamp) + self.receiver).encode()
        print('hash it>>>>>>>>>>>>>>>>>>>>>>> ',hash_it)
        return hashlib.sha256(hash_it).hexdigest()

def sign_transaction(trans_obj, sender_obj):
    print('=========================',sender_obj.exists, sender_obj.login, sender_obj.balance - trans_obj.amount)
    if sender_obj.exists and sender_obj.login and (sender_obj.balance - trans_obj.amount) > 0:
            print('-----------Transaction Signed')
            trans_obj.signature = True
            return True
    else:
        print('---------------Cannot Sign Transaction')
        trans_obj.signature = False

# def validate_trans(trans_obj):
#         if not trans_obj.signature or (trans_obj.hash != trans_obj.generate_hash()):
#             print('INVALID TRANSACTION')
#             return False
#         return True
