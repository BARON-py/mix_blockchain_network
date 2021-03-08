from wallet import Ecdsa , PrivateKey

from node.myownp2pn import MyOwnPeer2PeerNode


def send(my_public_key,my_private_key,to_user, data = None,amount = None):
  from blockchain.blockchain_main import get_blockchain
  get_blockchain().createTrans(signature = Ecdsa.sign(str(my_public_key)+str(to_user)+str(data)+str(amount), PrivateKey.fromPem(my_private_key)).toBase64(),fromUser = str(my_public_key),toUser = str(to_user),data = str(data),amount = amount,processing_fee = 1)