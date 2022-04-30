from django.test import TestCase
from views.block import Block
from views.transaction import Transaction, validate_trans
from views.user_block import UserBlock
# Create your tests here.

class TestBlock:
    def __init__(self, hash):
        self.trans_hash = hash


trans_obj = []
trans_obj.append(TestBlock('1234'))

create_block = Block(trans_obj, '1')

print('------block created----- ')
print(create_block.primary_ky)
print(create_block.prev_blk_hash)
print(create_block.blk_data)
print(create_block.nonce)
print(create_block.curr_blk_hash)
print('---------mining----------')
trans_obj.append(TestBlock('1235'))
Block(trans_obj, '2').mining_the_block()

transaction_obj = Transaction('me', 'you', 1000)
validate_trans(transaction_obj)

user = UserBlock('Alice', 'fakepassword')

Transaction('Alice', 'Bob', 1000).sign_transaction(user)

user = UserBlock('CrazyMiner', 'truepassword')
user.exists = True
user.login = True

Transaction('CrazyMiner', 'Bob', 1000).sign_transaction(user)

Transaction('CrazyMiner', 'Bob', 90).sign_transaction(user)