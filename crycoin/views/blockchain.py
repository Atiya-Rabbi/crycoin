from datetime import datetime
import requests
from crycoin.views.transaction import Transaction
from crycoin.views.block import Block
from urllib.parse import urlparse


class Blockchain (object):
    def __init__(self):
        self.chain = [self.addGenesisBlock()]
        self.pendingTransactions = []
        self.minerRewards = 50
        self.blockSize = 10
        self.nodes = set()
        
    def getLastBlock(self):

        return self.chain[-1]

    def addGenesisBlock(self):
        tArr = []
        tArr.append(Transaction("me", "you", 10))
        genesis = Block(tArr, 0)

        genesis.prev = "None"
        return genesis

    def register_node(self, address):
        parsedUrl = urlparse(address)
        self.nodes.add(parsedUrl.netloc)
        print(parsedUrl.netloc)

    def resolveConflicts(self):
        neighbors = self.nodes;
        newChain = None;

        maxLength = len(self.chain);

        for node in neighbors:
            response = requests.get(f'http://{node}/chain');
            print('my res---->',response)
            if response.status_code == 200:
                # print(response['length'])
                length = response.json()['length'];
                chain = response.json()['chain'];

                if length > maxLength:
                    maxLength = length;
                    newChain = chain;

        if newChain:
            self.chain = self.chainJSONdecode(newChain);
            print(self.chain);
            return True;

        return False;

    def chainJSONdecode(self, chainJSON):
        chain=[];
        for blockJSON in chainJSON:

            tArr = [];
            for tJSON in blockJSON['transactions']:
                print('sender---',tJSON['sender'])
                transaction = Transaction(tJSON['sender'], tJSON['receiver'], tJSON['amount']);
                transaction.time_stamp = tJSON['time_stamp'];
                transaction.hash = tJSON['hash'];
                tArr.append(transaction);


            block = Block(tArr, blockJSON['primary_ky'], blockJSON['time']);
            block.curr_blk_hash = blockJSON['curr_blk_hash'];
            block.prev_blk_hash =blockJSON['prev_blk_hash'];
            block.nonce = blockJSON['nonce'];

            chain.append(block);
        return chain;

    def chainJSONencode(self):

        blockArrJSON = [];
        for block in self.chain:
            blockJSON = {};
            blockJSON['curr_blk_hash'] = block.curr_blk_hash;
            blockJSON['primary_ky'] = block.primary_ky;
            blockJSON['prev_blk_hash'] = block.prev_blk_hash;
            blockJSON['time'] = block.time;
            blockJSON['nonce'] = block.nonce;


            transactionsJSON = [];
            
            for transaction in block.blk_data:
                tJSON = {};
                # print('sender--', transaction.sender)
                tJSON['time_stamp'] = transaction.time_stamp;
                tJSON['sender'] = transaction.sender;
                tJSON['receiver'] = transaction.receiver;
                tJSON['amount'] = transaction.amount;
                tJSON['hash'] = transaction.hash;
                transactionsJSON.append(tJSON);

            blockJSON['transactions'] = transactionsJSON;
            # print('-----------',blockJSON['transactions'])
            blockArrJSON.append(blockJSON);

        return blockArrJSON;
