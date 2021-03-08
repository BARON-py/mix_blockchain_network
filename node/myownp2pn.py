from node.node import *
import pickle

from wallet import Signature ,  Wallet_Import

from lib.mixlib import dprint




class MyOwnPeer2PeerNode (Node):
    main_node = None
    # Python class constructor
    def __init__(self, host, port):
        self.__class__.main_node = self
        super(MyOwnPeer2PeerNode, self).__init__(host, port, None)
        print("MyPeer2PeerNode: Started")


    # all the methods below are called when things happen in the network.
    # implement your network node behavior to create the required functionality.

    def outbound_node_connected(self, node):
        print("outbound_node_connected: " + node.id)
        
    def inbound_node_connected(self, node):
        print("inbound_node_connected: " + node.id)

    def inbound_node_disconnected(self, node):
      
        print("inbound_node_disconnected: " + node.id)

    def outbound_node_disconnected(self, node):
        
        print("outbound_node_disconnected: " + node.id)

    def node_message(self, node, data):
        if str(data) == "sendmefullchain":
            self.send_full_chain(node)
        print("Data Type: "+str(type(data))+"\n")

        if str(data) == "sendmefullnodelist":
            self.send_full_node_list(node)
        print("Data Type: "+str(type(data))+"\n")

        try:
            if data["fullchain"] == 1:
                print("getting chain")
                self.get_full_chain(data["byte"])
        except:
            pass

        try:
            if data["fullnodelist"] == 1:
                print("getting node list")
                self.get_full_node_list(data["byte"])
        except:
            pass

        try:
         if data["transactionrequest"]  == 1:
            self.get_transaction(data)
        except:
            pass
        try:
         if data["block_finded"] == 1:
            self.block_finded(data)
        except:
            pass


        print("node_message from " + node.id + ": " + str(data))
        
    def node_disconnect_with_outbound_node(self, node):
        print("node wants to disconnect with oher outbound node: " + node.id)
        
    def node_request_to_stop(self):
        print("node is requested to stop!")

    def send_full_chain(self,node = None):
        dprint("Sending full chain to node or nodes."+" Node: "+ str(node))
        file = open("blockchain.mix_blockchain_network", "rb")
        SendData = file.read(1024)
        while SendData:

            data = {"fullchain" : 1,"byte" : (SendData.decode(encoding='iso-8859-1'))}
            if not node == None:
                self.send_to_node(node,data)
            else:
                self.send_to_nodes(data)

            SendData = file.read(1024) 
    def get_full_chain(self,data):
        
        file = open("blockchain.mix_blockchain_network", "ab")

        file.write((data.encode(encoding='iso-8859-1')))

        file.close()

    def send_full_node_list(self,node = None):
        print("nice")
        file = open("connected_node.mix_blockchain_network", "rb")
        SendData = file.read(1024)
        while SendData:

            data = {"fullchain" : 1,"byte" : (SendData.decode(encoding='iso-8859-1'))}
            print(data)
            print(type(data))
            if not node == None:
                self.send_to_node(node,data)
            else:
                self.send_to_nodes(data)

            SendData = file.read(1024) 
    def get_full_node_list(self,data):
        
        file = open("connected_node.mix_blockchain_network", "ab")

        file.write((data.encode(encoding='iso-8859-1')))

        file.close()



    def get_transaction(self,data):
        from blockchain.blockchain_main import get_blockchain
        print("getting transactions")
        system = get_blockchain()
        print(system)
        system.createTrans(signature =data["signature"],fromUser = data["fromUser"],toUser = data["to_user"],data = data["data"],amount = data["amount"],processing_fee = data["processing_fee"],transaction_sender="node")
        system.minePendingTrans(Wallet_Import(0,0))

    def block_finded(self,data):
        from blockchain.blockchain_main import get_blockchain
        system = get_blockchain()
        system.minePendingTrans(data["block_miner"],data["block_difficultyIncrement"])


