import random
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from crycoin.views.block import Block
from flask import request
from crycoin.views.user_block import UserBlock
from crycoin.views.blockchain import Blockchain
from crycoin import obj
from crycoin import balance
from crycoin.views.generate_trans import generate_trans
# from ..models import *
from django.http import JsonResponse

# Create your views here.
def view_transaction(request):
    global trans_list
    trans_list = generate_trans()
    return render(request, "crycoin/view_transaction.html", {
                "trans_list": trans_list,
                "balance": balance.current_balance,
            })

def blockchain_view(request):
    print(obj.nodes)
    consensus()
    return render(request, "crycoin/mine.html", {"blockchain": obj.chain, "balance": balance.current_balance,})

def chain(request):
    response = {
        'chain': obj.chainJSONencode(),
        'length': len(obj.chain),
    }
    print(response)
    return JsonResponse(response)

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        
        # Attempt to create new user
        user_obj = UserBlock(username, password)
        if user_obj.exists:
            return render(request, "crycoin/register.html", {
                "message": "Username already taken."
            })
        else:
            user_obj.exists = True
            user_obj.login = True

        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "crycoin/register.html")

def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]

        user_obj = UserBlock(username, password)
        if user_obj.exists:
            user_obj.login = True
            return HttpResponseRedirect(reverse("index"))
        else:
            print('Invalid username and/or password.')
            return render(request, "crycoin/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "crycoin/login.html")

def logout_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]

        user_obj = UserBlock(username, password)
        if user_obj.exists:
            user_obj.login = False
    return HttpResponseRedirect(reverse("index"))

def mine(request):
    transaction_list = trans_list
    newBlock = Block(transaction_list, len(obj.chain))
    newBlock.mining_the_block()
    hashVal = obj.getLastBlock().curr_blk_hash;
    newBlock.prev_blk_hash = hashVal;
    obj.pendingTransactions = transaction_list
    obj.chain.append(newBlock);
    print('feedback-->',newBlock)
    print(obj)
    balance.add_balance()
    
    return render(request, "crycoin/mine.html", {'newBlock':newBlock, "balance": balance.current_balance, "message": 'Miner reward added!'})

def register_nodes(request):
    if request.method == "POST":
        node = request.POST["node"]
        # nodes = ['http://127.0.0.1:8002/']
        if node is None:
            return HttpResponse("Error: Please supply a valid list of nodes"), 400

        # for node in nodes:
        #     print('---------------->>',node)
        obj.register_node(node)

        response = {
            'message': 'New nodes have been added',
            'total_nodes': list(obj.nodes),
        }
        print(response)
        return render(request, "crycoin/login.html", response)
    return render(request, "crycoin/login.html")
    

def consensus():
    replaced = obj.resolveConflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': obj.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': obj.chain
        }
    print('RESPOPNSE---',response)
    # return HttpResponse(response)