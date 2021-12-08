import socket
import json
import numpy as np
from tensorflow import keras
from tensorflow.keras import layers
from tqdm import tqdm

import sys


clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

IP = '127.0.0.1'
PORT = 5005

# connect to the server
clientsocket.connect( (IP, PORT) )


# ---------------------------------SEQUENCE BEGINS-------------------------------------------

# Intro Message from server
print(clientsocket.recv(1024).decode())   # --> Welcome message from server

# send back an OK response to proceed with the sequence
#clientsocket.send('OK'.encode())


with np.load('mnist.npz', allow_pickle=True) as f:
    x_train, y_train = f['x_train'], f['y_train']
    x_test, y_test = f['x_test'], f['y_test']

    # x_train
    # --------------------------------------

    print('========================')
    print('Sending Training Samples')
    print('========================')

    batch = x_train[0:10].tolist()
    data = json.dumps(batch)
    clientsocket.send(data.encode())
    print(clientsocket.recv(1024).decode())

    for i in tqdm(range(10,10000,10)):
        batch = x_train[i:i+10].tolist()
        data = json.dumps(batch)
        clientsocket.send(data.encode())
        clientsocket.recv(1024).decode()
        #print(clientsocket.recv(1024).decode())

    # y_train
    # --------------------------------------

    print('=======================')
    print('Sending Training Lables')
    print('=======================')

    batch = y_train[0:10].tolist()
    data = json.dumps(batch)
    clientsocket.send(data.encode())
    print(clientsocket.recv(1024).decode())

    for i in tqdm(range(10,10000,10)):
        batch = y_train[i:i+10].tolist()
        data = json.dumps(batch)
        clientsocket.send(data.encode())
        clientsocket.recv(1024).decode()
        #print(clientsocket.recv(1024).decode())


    # x_test
    # --------------------------------------

    print('=======================')
    print('Sending Testing Samples')
    print('=======================')

    batch = x_test[0:10].tolist()
    data = json.dumps(batch)
    clientsocket.send(data.encode())
    print(clientsocket.recv(1024).decode())

    for i in tqdm(range(10,1000,10)):
        batch = x_test[i:i+10].tolist()
        data = json.dumps(batch)
        clientsocket.send(data.encode())
        clientsocket.recv(1024).decode()
        #print(clientsocket.recv(1024).decode())

    # y_test
    # --------------------------------------

    print('======================')
    print('Sending Testing Lables')
    print('======================')

    batch = y_test[0:10].tolist()
    data = json.dumps(batch)
    clientsocket.send(data.encode())
    print(clientsocket.recv(1024).decode())

    for i in tqdm(range(10,1000,10)):
        batch = y_test[i:i+10].tolist()
        data = json.dumps(batch)
        clientsocket.send(data.encode())
        clientsocket.recv(1024).decode()
        #print(clientsocket.recv(1024).decode())




