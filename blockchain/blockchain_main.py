import datetime
import hashlib

import pprint

from wallet import Ecdsa , PublicKey , Wallet_Import , Signature

import pickle


from blockchain.merkleroot import mixmerkletree


from lib.settings import the_settings
from lib.mixlib import dprint


class Block:
    def __init__(self, timeStamp, trans,miner,reward, previousBlock = ''):
        self.timeStamp = timeStamp
        self.trans = trans
        self.previousBlock = previousBlock
        self.difficultyIncrement = 0
        self.hash = self.calculateHash(trans, timeStamp, self.difficultyIncrement)
        self.miner = miner
        self.reward = reward
 
    def calculateHash(self, data, timeStamp, difficultyIncrement):
        """
        data = str(data) + str(timeStamp) + str(difficultyIncrement)
        data = data.encode()
        hash = hashlib.sha256(data)
        return hash.hexdigest()
        """
        return mixmerkletree([str(data),str(timeStamp),str(difficultyIncrement)]).getRootHash()
    def mineBlock(self,difficulty,difficultyIncrement = None):
        difficultyCheck = "9" * difficulty
        while self.hash[:difficulty] != difficultyCheck:   
            """ 
            print("self.hash[:difficulty]: "+str(self.hash[:difficulty]))
            print("difficultyCheck: "+str(difficultyCheck))
            print("self.difficultyIncrement: "+str(self.difficultyIncrement))
            """
            self.hash = self.calculateHash(self.trans,self.timeStamp,self.difficultyIncrement)
            self.difficultyIncrement = self.difficultyIncrement + 1 
 
class Blockchain:
    def __init__(self):
        self.chain = []
        self.difficulty = 1 #5
        self.reward = 10
        self.data_sending_fee = 1
        self.pendingTransaction = []

        self.GenesisBlock()
    def GenesisBlock(self):
        dprint("Creating genesis block.")
        self.pendingTransaction.append(Transaction("SYSTEM","SYSTEM","SYSTEM",data = "Hello world i am genesis block.",amount = 0,processing_fee=0))
        #genesisBlock = Block(str(datetime.datetime.now()),"I am the Gensis Block")
        #return genesisBlock
 
    def getLastBlock(self):
        return self.chain[len(self.chain) - 1]
    def minePendingTrans(self,miner,difficultyIncrement = None):
      if not len(self.pendingTransaction) < 3 or len(self.chain) == 0 or difficultyIncrement != None: # burası olmadığından işlenmiyor burayı transfer isteği attığımızda kendimizede pending transaction olarak yazıcaz şekilde yapıcaz ama mining etmeden önce mutlaka diğer nodelarada bildiri yapıcaz
        dprint("Starting mining procces.")
        #in reality not all of the pending transaction go into the block the miner gets to pick which one to mine
        block_reward = self.reward
        for element in self.pendingTransaction:
            block_reward += element.processing_fee
        newBlock = Block(str(datetime.datetime.now()),self.pendingTransaction,miner=miner,reward=block_reward)     
        if not difficultyIncrement == None:
            newBlock.mineBlock(self.difficulty,difficultyIncrement)
        else:
            newBlock.mineBlock(self.difficulty)
        newBlock.previousBlock = self.getLastBlock().hash if not len(self.chain) == 0 else ""
 
        dprint("Previous Block's Hash: " + newBlock.previousBlock)
        testChain = []
        for trans in newBlock.trans:
            temp = str(trans.__dict__)
            testChain.append(temp)
        #pprint.pprint(testChain)
 

        #this
        self.chain.append(newBlock)
        dprint("Block's Hash: " + newBlock.hash)
        dprint("Block added")
        self.pendingTransaction = []
        self.save_blockchain()
        if difficultyIncrement == None:
            from node.myownp2pn import MyOwnPeer2PeerNode
            if len(self.chain) > 1:
                dprint("Mined block is sending the other node.")
                MyOwnPeer2PeerNode.main_node.send_to_nodes({"block_finded" : 1,"block_miner" : newBlock.miner,"block_difficultyIncrement" : newBlock.difficultyIncrement})
            else:
                MyOwnPeer2PeerNode.main_node.send_full_chain()
    def isChainValid(self):
        for x in range(1,len(self.chain)):
            currentBlock = self.chain[x]
            previousBlock = self.chain[x-1]
 
            if (currentBlock.previousBlock != previousBlock.hash):
                print("*** The Chain is not valid! ***")
        print("*** The Chain is valid and secure ***")

    def createTrans(self,signature, fromUser,toUser,processing_fee,data = None, amount = None,transaction_sender = None):
      dprint("Creating transaction.")
      signature_class = Signature.fromBase64(signature)
      dprint("***")
      dprint(signature)
      dprint(fromUser)
      dprint(toUser)
      dprint(processing_fee)
      dprint(data)
      dprint(amount)
      dprint("***")
      dprint(Ecdsa.verify((str(fromUser)+str(toUser)+str(data)+str(amount)), signature_class, PublicKey.fromPem(fromUser)))
      if Ecdsa.verify((str(fromUser)+str(toUser)+str(data)+str(amount)), signature_class, PublicKey.fromPem(fromUser)):
          dprint("Sign verify is true.")
          if self.getBalance(fromUser) >= (float(amount)+float(processing_fee)) and (float(amount)+float(processing_fee)) != float(0): #test et
               dprint("Balance controll is true.")
               self.pendingTransaction.append(Transaction(signature_class.toBase64(),fromUser,toUser,data = data,amount = amount,processing_fee=processing_fee))

               self.save_blockchain()
               if transaction_sender != "node":
                   from node.myownp2pn import MyOwnPeer2PeerNode
                   MyOwnPeer2PeerNode.main_node.send_to_nodes({"transactionrequest" : 1, "signature" : signature, "fromUser" : fromUser , "to_user" : toUser, "data" : data, "amount" : amount, "processing_fee" : processing_fee})
               return True
 
    def print_chain(self):
      result = ""
      for element in self.chain:
        result += str(element.__dict__)
      print(result)
    def print_transactions(self):
      result = ""
      for element in self.chain:
        if not isinstance(element.trans, str) :
         for trans_element in element.trans:
          result += str(trans_element.__dict__)
      print(result)
 
 
    def getBalance(self,user):
        balance = 0
        for block in self.chain:
            if block.miner == user:
                balance += block.reward
            for transaction in block.trans:
                if transaction.fromUser == user:
                    balance -= float(transaction.amount)
                    balance -= float(transaction.processing_fee)
                if transaction.toUser == user:
                    balance += float(transaction.amount)
        return balance

    def save_blockchain(self):
        from config import get_config
        import os
        old_cwd = os.getcwd()
        os.chdir(get_config().main_folder)
        with open('blockchain.mix_blockchain_network', 'wb') as blockchain_file:
            pickle.dump(self, blockchain_file,protocol=2)
        os.chdir(old_cwd)

 
 
class Transaction:
    def __init__(self,signature,fromUser,toUser,data,amount,processing_fee):
        self.signature = signature
        self.fromUser = fromUser
        self.toUser = toUser
        self.data = data
        self.amount = amount
        self.processing_fee = processing_fee





def get_blockchain():
        from config import get_config
        import os
        old_cwd = os.getcwd()
        os.chdir(get_config().main_folder)
        with open('blockchain.mix_blockchain_network', 'rb') as blockchain_file:
            return pickle.load(blockchain_file)
        os.chdir(old_cwd)




def sendme_full_node_list():
    from node.myownp2pn import MyOwnPeer2PeerNode
    node = MyOwnPeer2PeerNode.main_node
    node.send_to_node(node.nodes_outbound[0],"sendmefullnodelist")  


def sendme_full_chain():
    from node.myownp2pn import MyOwnPeer2PeerNode
    node = MyOwnPeer2PeerNode.main_node
    node.send_to_node(node.nodes_outbound[0],"sendmefullchain")   


def create_blockchain():
    
    if the_settings().test_mode() == True:
        dprint("Creating new blockchain")
        system = Blockchain()
        system.minePendingTrans(Wallet_Import(0,0))
    else:
        dprint("Getting blockchain from nodes")
        sendme_full_chain()