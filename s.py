import socket
import json
import numpy as np
from tensorflow import keras
from tensorflow.keras import layers
from tqdm import tqdm

# instantiate server's socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# define address params
IP = '127.0.0.1'
PORT = 5005

# bind server
serversocket.bind( (IP, PORT) )

# start listening
serversocket.listen()


print('The server is up! Listening at:',IP,PORT)
print()


# ----------------- DATA -------------------


view_count = 0
# every time a new user connects, we increase view count by 1

# ------------------------------------------

def handle_new_client(clientsocket, address):

    global random_facts
    global view_count

    with np.load('mnist.npz', allow_pickle=True) as f:
        x_train, y_train = f['x_train'], f['y_train']
        x_test, y_test = f['x_test'], f['y_test']


    print('-------------------------------------------')
    print('New connection made! Client address:',address)


    # interact with client
    # --------------------------------------------------------------

    # send intro message
    intro = 'Welcome to the FedML!\n'

    clientsocket.send(intro.encode())

    # wait for OK response
    if clientsocket.recv(1024).decode() != 'OK':
        print('Something went wrong! Disconnecting')
        clientsocket.close()


    # x_train
    # --------------------------------------
    batch = x_train[0:10].tolist()
    data = json.dumps(batch)
    clientsocket.send(data.encode())
    print(clientsocket.recv(1024).decode())

    for i in tqdm(range(10,1000,10)):
        batch = x_train[i:i+10].tolist()
        data = json.dumps(batch)
        clientsocket.send(data.encode())
        clientsocket.recv(1024).decode()
        #print(clientsocket.recv(1024).decode())

    # y_train
    # --------------------------------------
    batch = y_train[0:10].tolist()
    data = json.dumps(batch)
    clientsocket.send(data.encode())
    print(clientsocket.recv(1024).decode())

    for i in tqdm(range(10,1000,10)):
        batch = y_train[i:i+10].tolist()
        data = json.dumps(batch)
        clientsocket.send(data.encode())
        clientsocket.recv(1024).decode()
        #print(clientsocket.recv(1024).decode())


    # x_test
    # --------------------------------------
    batch = x_test[0:10].tolist()
    data = json.dumps(batch)
    clientsocket.send(data.encode())
    print(clientsocket.recv(1024).decode())

    for i in tqdm(range(10,100,10)):
        batch = x_test[i:i+10].tolist()
        data = json.dumps(batch)
        clientsocket.send(data.encode())
        clientsocket.recv(1024).decode()
        #print(clientsocket.recv(1024).decode())

    # y_test
    # --------------------------------------
    batch = y_test[0:10].tolist()
    data = json.dumps(batch)
    clientsocket.send(data.encode())
    print(clientsocket.recv(1024).decode())

    for i in tqdm(range(10,100,10)):
        batch = y_test[i:i+10].tolist()
        data = json.dumps(batch)
        clientsocket.send(data.encode())
        clientsocket.recv(1024).decode()
        #print(clientsocket.recv(1024).decode())


    # -------------------------------------------------------------

    

    weights = [None]*6
    
    for i in tqdm(range(0,6)):
        if i == 4 or i == 2:
            print("Avoid")
        else: 
            clientsocket.send("OK".encode())
            weights[i] = np.array(json.loads(clientsocket.recv(100000000).decode()))
            print(weights[i].shape)
            print(type(weights[i]))

    #print(weights)

    '''

    model = keras.Sequential(
    [
        keras.Input(shape = (28, 28, 1)),
        layers.Conv2D(32, kernel_size=(3, 3), activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Flatten(),
        layers.Dropout(0.5),
        layers.Dense(10, activation="softmax"),
    ]
    )
    model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
    model.set_weights(weights)
    
    #model.evaluate(x_test, y_test, verbose=0)
    #model.load_weights('my_checkpoint')

    score = model.evaluate(x_test, y_test, verbose=0)
    print("Test loss:", score[0])
    print("Test accuracy:", score[1])
    #print("Test loss:", score[0])
    #print("Test accuracy:", score[1])

    '''

    print('Disconnecting from client!')
    # print()
    view_count += 1
    print('Total view count:',view_count)
    print()


while True:

    # wait until a client connects
    (clientsocket, address) = serversocket.accept() #--> returns (clientsocket, address)

    # we won't reach this point until a client connects
    
    # call the "handle_new_client" function to interact with the client
    handle_new_client(clientsocket,address)

    clientsocket.close()    # close the connection and start the next iteration of the loop to wait for the next client





print('The server is going down!')
serversocket.close()    # close down the server


