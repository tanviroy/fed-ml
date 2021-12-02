import socket
import json
from pickle import dumps, loads
import numpy as np

clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

IP = '127.0.0.1'
PORT = 5545

# connect to the server
clientsocket.connect( (IP, PORT) )


# ---------------------------------SEQUENCE BEGINS-------------------------------------------

# wait for intro message
print(clientsocket.recv(1024).decode())   # --> returns a string

# send back an OK response to proceed with the sequence
clientsocket.send('OK'.encode())


# wait for random facts
#facts = clientsocket.recv(1024).decode()
facts = clientsocket.recv(10000)
facts = loads(facts)
for i in range(0,5):
    facts = np.concatenate((facts, loads(clientsocket.recv(10000))))
print('----------------------------')
print('Our set of facts!')
print('----------------------------')
print("x_train shape:", facts.shape)
print(type(facts))

#for fact in facts:
#    print(fact[0], '- ('+fact[1]+')')     # print fact along with signature in brackets




#print('\n\nWould you like to add a fact? (Y/N): ',end='')
# ask user if they want to add a fact
#choice = input()

clientsocket.send('N'.encode())  # send choice to server