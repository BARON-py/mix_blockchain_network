from func.send import send

from wallet import Wallet_Import

def send_coin(coin_amount,to_user):
  my_public_key = Wallet_Import(0,0)
  my_private_key = Wallet_Import(0,1)
  if isinstance(int(coin_amount), int) or isinstance(float(coin_amount), float):
   print("sendcoin"+str(coin_amount))
   send(my_public_key=my_public_key,my_private_key=my_private_key,to_user=to_user, amount = coin_amount)
  else:
    print("This is not integer coin amount.")