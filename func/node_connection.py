from node.myownp2pn import MyOwnPeer2PeerNode
from lib.settings import the_settings

def ndstart(port):
    node = MyOwnPeer2PeerNode("",port)
    node.debug = the_settings().debug_mode()
    node.start()     

def ndstop():
    MyOwnPeer2PeerNode.main_node.stop()

def ndconnect(ip,port):
    MyOwnPeer2PeerNode.main_node.connect_with_node(ip, port)


def ndconnectmix_blockchain_network():
    MyOwnPeer2PeerNode.main_node.connectionfrommix_blockchain_network()