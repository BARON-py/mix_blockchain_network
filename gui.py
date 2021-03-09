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

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import simpledialog, messagebox

class main_gui:
    def __init__(self, master=None):
        # build ui
        self.toplevel = tk.Tk() if master is None else tk.Toplevel(master)
        self.frame = ttk.Frame(self.toplevel)
        self.create_blockchain_button = ttk.Button(self.frame)
        self.blockchain_44x50_png = tk.PhotoImage(file='gui/icons/blockchain_44x50.png')
        self.create_blockchain_button.configure(compound='top', image=self.blockchain_44x50_png, text='Create Blockchain')
        self.create_blockchain_button.grid(column='0', padx='25', pady='20', row='2', sticky='w')
        self.create_blockchain_button.configure(command=self.create_blockchain)
        self.create_wallet_button = ttk.Button(self.frame)
        self.wallet_60x50_png = tk.PhotoImage(file='gui/icons/wallet_60x50.png')
        self.create_wallet_button.configure(compound='top', image=self.wallet_60x50_png, text='Create Wallet')
        self.create_wallet_button.grid(column='2', padx='25', pady='20', row='2', sticky='e')
        self.create_wallet_button.configure(command=self.Wallet_Create)
        self.send_coin_button = ttk.Button(self.frame)
        self.money_67x50_png = tk.PhotoImage(file='gui/icons/money_67x50.png')
        self.send_coin_button.configure(compound='top', image=self.money_67x50_png, text='Send Coin')
        self.send_coin_button.grid(column='0', padx='25', pady='20', row='3', sticky='w')
        self.send_coin_button.configure(command=self.send_coin)
        self.send_message_button = ttk.Button(self.frame)
        self.emails_65x50_png = tk.PhotoImage(file='gui/icons/emails_65x50.png')
        self.send_message_button.configure(compound='top', image=self.emails_65x50_png, text='Send Message')
        self.send_message_button.grid(column='2', padx='25', pady='20', row='3', sticky='e')
        self.send_message_button.configure(command=self.send_message)
        self.balance_label = ttk.Label(self.frame)
        self.balance_label.configure(text='Balance: ')
        self.balance_label.grid(column='0', ipadx='25', padx='25', pady='20', row='6', sticky='sw')
        self.reflesh_balance_button = ttk.Button(self.frame)
        self.reflesh_balance_button.configure(compound='top', text='Reflesh Balance')
        self.reflesh_balance_button.grid(column='3', padx='25', pady='20', row='6', sticky='se')
        self.reflesh_balance_button.configure(command=self.reflesh_balance)
        self.button1 = ttk.Button(self.frame)
        self.cellmolecule_50x50_png = tk.PhotoImage(file='gui/icons/cell-molecule_50x50.png')
        self.button1.configure(compound='top', image=self.cellmolecule_50x50_png, text='Connect Node')
        self.button1.grid(column='3', padx='25', pady='20', row='2', sticky='e')
        self.button1.configure(command=self.connect_node)
        self.button2 = ttk.Button(self.frame)
        self.computerinternetnetwork_68x50_png = tk.PhotoImage(file='gui/icons/computer-internet-network_68x50.png')
        self.button2.configure(compound='top', image=self.computerinternetnetwork_68x50_png, text='Start Node Server')
        self.button2.grid(column='0', padx='25', pady='20', row='4', sticky='w')
        self.button2.configure(command=self.start_node_server)
        self.button3 = ttk.Button(self.frame)
        self.button3.configure(compound='top', image=self.cellmolecule_50x50_png, text='Connect Node \nfrom mix_blockchain_network \ndatabase')
        self.button3.grid(column='3', padx='25', pady='20', row='3', sticky='e')
        self.button3.configure(command=self.connect_node_mix_blockchain_network)
        self.button4 = ttk.Button(self.frame)
        self.button4.configure(compound='top', text='Test Mode ON')
        self.button4.grid(column='3', padx='25', pady='20', row='4', sticky='e')
        self.button4.configure(command=self.test_mode_on)
        self.button6 = ttk.Button(self.frame)
        self.button6.configure(compound='top', text='Test Mode OFF')
        self.button6.grid(column='3', padx='25', pady='20', row='5', sticky='e')
        self.button6.configure(command=self.test_mode_off)
        self.button7 = ttk.Button(self.frame)
        self.button7.configure(compound='top', image=self.computerinternetnetwork_68x50_png, text='Stop Node Server')
        self.button7.grid(column='2', padx='25', pady='20', row='4', sticky='e')
        self.button7.configure(command=self.stop_node_server)
        self.frame.configure(height='200', width='200')
        self.frame.grid(column='0', row='0')
        self.toplevel.configure(height='200', takefocus=True, width='200')
        self.toplevel.iconphoto(True, self.blockchain_44x50_png)
        self.toplevel.resizable(True, True)
        self.toplevel.title('Mix Blockchain Network')

        # Main widget
        self.mainwindow = self.toplevel


    def create_blockchain(self):
        create_blockchain()
        messagebox.showinfo('Wallet', 'Blockchain are created.')

    def Wallet_Create(self):
        Wallet_Create()
        messagebox.showinfo('Wallet', 'Wallet are created.')
    
    def send_coin(self):
        
        received_adress = simpledialog.askstring("Input", "Please write receiver adress: ",
                                parent=self.toplevel)
        if received_adress is not None:
            print("Receiver adress: ", received_adress)
        else:
            print("You don't write a receiver adress ?")
        
        amount = simpledialog.askfloat("Input", "Coin Amount: ",
                               parent=self.toplevel,
                               minvalue=0.0, maxvalue=100000.0)
        
        if amount is not None:
            print("Coin Amount: ", amount)
        else:
            print("You don't write a coin amount ?")
        
        okey = messagebox.askokcancel("Okey",("Receiver adress: "+received_adress+"\n"+"Amount: "+str(amount)))

        if okey:
            send_coin(amount,received_adress)

    def send_message(self):
        received_adress = simpledialog.askstring("Input", "Please write receiver adress: ",
                                parent=self.toplevel)
        if received_adress is not None:
            print("Receiver adress: ", received_adress)
        else:
            print("You don't write a receiver adress ?")
        
        message = simpledialog.askstring("Input", "Please write message: ",
                                parent=self.toplevel)
        if message is not None:
            print("Message: ", message)
        else:
            print("You don't write a message ?")
        
        okey = messagebox.askokcancel("Okey",("Receiver adress: "+received_adress+"\n"+"Message: "+message))

        if okey:
            send_message(message,received_adress)

    def reflesh_balance(self):
        self.balance_label.configure(text=("Balance: "+str(get_blockchain().getBalance(Wallet_Import(0,0)))))
        
    def connect_node(self):
        ip = simpledialog.askstring("Input", "IP: ",
                                 parent=self.toplevel)
        if ip is not None:
            print("IP: ", ip)
        else:
            print("You don't write ip ?")


        port = simpledialog.askinteger("Input", "Port: ",
                                 parent=self.toplevel,
                                 minvalue=0, maxvalue=65353)
        if port is not None:
            print("Port: ", port)
        else:
            print("You don't write port ?")

        ndconnect(ip,port)

        messagebox.showinfo('Node', ("Connected Node on "+"IP:"+ip+" PORT: "+str(port)+"."))

    def start_node_server(self):
        port = simpledialog.askinteger("Input", "Port: ",
                                 parent=self.toplevel,
                                 minvalue=0, maxvalue=65353)
        if port is not None:
            print("Port: ", port)
        else:
            print("You don't write port ?")

        ndstart(port)
        messagebox.showinfo('Node', ('Node server is started on '+str(port)+"."))

    def connect_node_mix_blockchain_network(self):
        ndconnectmix_blockchain_network()
        messagebox.showinfo('Node', 'Connected Node or Nodes from mix_blockchain_network database.')

    def test_mode_on(self):
        the_settings().test_mode(True)
        messagebox.showinfo('Node', 'Test mode is ON')

    def test_mode_off(self):
        the_settings().test_mode(False)
        messagebox.showinfo('Node', 'Test mode is OFF')

    def stop_node_server(self):
        ndstop()
        messagebox.showinfo('Node', 'Node server is stoped.')
    def run(self):
        self.mainwindow.mainloop()
        





def start():
    app = main_gui()
    app.run() 

if __name__ == '__main__':
    start()
    







"""
messagebox.showerror("Answer", "Sorry, no answer available")

messagebox.showwarning('Yes', 'Not yet implemented')
messagebox.showinfo('Wallet', 'Wallet are created.')


answer = simpledialog.askinteger("Input", "What is your age?",
                                 parent=application_window,
                                 minvalue=0, maxvalue=100)
if answer is not None:
    print("Your age is ", answer)
else:
    print("You don't have an age?")
"""





"""
answer = messagebox.askretrycancel("Question", "Do you want to try that again?")
answer = messagebox.askyesno("Question","Do you like Python?")
answer = messagebox.askyesnocancel("Question", "Continue playing?")
"""