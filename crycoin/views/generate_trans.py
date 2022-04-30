
from crycoin.views.user_block import UserBlock
from crycoin.views.transaction import Transaction, sign_transaction
import random

def generate_trans():
    sender_list = ['Gabbar Singh','Bhiku Mhatre','Vijay Dinanath Chauhan','Anand','Mogambo','PK','Albert Pinto','Raj','Munna Rangeela','Tara Singh','Rancho','Sardar Khan']
    receiver_list = ['Bhuvan','Simran','Chulbul Pnadey','Ameeran','Sher Khan','Babban','Jhilmil','Dr. Viru Sahastrabuddhi','Faizal Khan','Langda Tyagi','Kabir Khan','Choocha']
    trans_list = []
    random.shuffle(sender_list)
    random.shuffle(receiver_list)

    for i in range(12):
        user = UserBlock(sender_list[i], 'truepassword')
        user.exists = True
        user.login = True
        trans_obj = Transaction(sender_list[i], receiver_list[i], random.randint(1,100))
        
        print(trans_obj)
        if sign_transaction(trans_obj,user):
            trans_list.append(trans_obj)
    print(trans_list)
    return trans_list