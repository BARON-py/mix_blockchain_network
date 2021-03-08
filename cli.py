import hashlib
import datetime
import json

import uuid

from hashlib import sha256


from sys import version_info as pyVersion
from binascii import hexlify, unhexlify

from wallet import *




from func.send_message import send_message
from func.send_coin import send_coin
from func.node_connection import *



from lib.mixlib import *

import pickle



from blockchain.blockchain_main import get_blockchain , create_blockchain, sendme_full_chain

from lib.settings import the_settings













def show_menu():
	print(banner_maker(sc_name="mix_blockchain_network Coin",description="This is new generation best safe coin.",author="Onur Atakan ULUSOY",email="atadogan06@gmail.com") + \
       menu_space() + \
       menu_maker(menu_number="cbc",menu_text="Create Blockchain")+ \
	   menu_maker(menu_number="cw",menu_text="Create Wallet")+ \
	   menu_space() + \
	   menu_maker(menu_number="sm",menu_text="Send Message")+ \
	   menu_maker(menu_number="sc",menu_text="Send Coin")+ \
	   menu_space() + \
       menu_maker(menu_number="gb",menu_text="Get Balance")+ \
       menu_space() + \
	   menu_maker(menu_number="ndstart",menu_text="Node Start")+ \
       menu_maker(menu_number="ndstop",menu_text="Node Stop")+ \
       menu_maker(menu_number="ndconnect",menu_text="Node Connect")+ \
       menu_maker(menu_number="ndconnectmix_blockchain_network",menu_text="Node Connect from mix_blockchain_network-DB")+ \
       menu_space() + \
       menu_maker(menu_number="testmodeon",menu_text="Test mode ON")+ \
       menu_maker(menu_number="testmodeoff",menu_text="Test mode OF")+ \
       menu_maker(menu_number="debugmodeon",menu_text="Debug mode ON")+ \
       menu_maker(menu_number="debugmodeoff",menu_text="Debug mode OF")+ \
       menu_space() + \
       menu_maker(menu_number="getfullnodelist",menu_text="Get Full Node List")+ \
       menu_maker(menu_number="getfullchain",menu_text="Get Full Chain")+ \
	  quit_menu_maker(mode="main")
	)


def menu():
    while True:
        show_menu()
        choices_input = question_maker(mode="main")


        if choices_input == "cbc":
            create_blockchain()
        if choices_input == "cw":
            Wallet_Create()
        if choices_input == "sm":
            send_message(input("Message: "),input("Please write receiver adress: "))
        if choices_input == "sc":
            send_coin(input("Coin Amount: "),input("Please write receiver adress: "))
        if choices_input == "gb":
            print(get_blockchain().getBalance(Wallet_Import(0,0)))
        if choices_input == "help":
            show_menu()
        if choices_input == "ndstart":
            ndstart(int(input("port: ")))
        if choices_input == "ndstop":
            ndstop()
        if choices_input == "ndconnect":
            ndconnect(str(input("node ip: ")),int(input("node port: ")))
        if choices_input == "ndconnectmix_blockchain_network":
            ndconnectmix_blockchain_network()
        if choices_input == "testmodeon":
            the_settings().test_mode(True)
        if choices_input == "testmodeoff":
            the_settings().test_mode(False)
        if choices_input == "debugmodeon":
            the_settings().debug_mode(True)
        if choices_input == "debugmodeoff":
            the_settings().debug_mode(False)


        if choices_input == "getfullnodelist":
            sendme_full_node_list()
        if choices_input == "getfullchain":
            sendme_full_chain()





        if choices_input == "0":
            exit() 

def start():
    menu()

if __name__ == '__main__':
    start()