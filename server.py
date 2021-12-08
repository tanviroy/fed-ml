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


def handle_new_client(clientsocket, address):

    print('New connection made! Client address:',address)

    # interact with client
    # --------------------------------------------------------------

    # send intro message
    intro = 'Welcome to the OutsourceML!\n'
    clientsocket.send(intro.encode())  # --> Intro message to connected client


    # x_train
    # -----------------------------------------

    print('==========================')
    print('Receiving Training Samples')
    print('==========================')

    batch = clientsocket.recv(1000000).decode()
    x_train = json.loads(batch)
    clientsocket.send('OK'.encode())
    #print(np.array(facts1).shape)

    for i in tqdm(range(10,10000,10)):

        batch = clientsocket.recv(1000000).decode()
        x_train = np.append(x_train, json.loads(batch),  axis = 0)
        clientsocket.send('OK'.encode())

    x_train = np.expand_dims(x_train, -1)
    print(np.array(x_train).shape)

    # y_train
    # -----------------------------------------

    print('==========================')
    print('Receiving Training Lables')
    print('==========================')

    batch = clientsocket.recv(1000000).decode()
    y_train = json.loads(batch)
    clientsocket.send('OK'.encode())
    #print(np.array(facts1).shape)

    for i in tqdm(range(10,10000,10)):
        batch = clientsocket.recv(1000000).decode()
        y_train = np.append(y_train, json.loads(batch),  axis = 0)
        clientsocket.send('OK'.encode())

    #y_train = np.expand_dims(y_train, -1)
    print(np.array(y_train).shape)


    # x_test
    # -----------------------------------------

    print('=========================')
    print('Receiving Testing Samples')
    print('=========================')

    batch = clientsocket.recv(1000000).decode()
    x_test = json.loads(batch)
    clientsocket.send('OK'.encode())
    #print(np.array(facts1).shape)

    for i in tqdm(range(10,1000,10)):
        batch = clientsocket.recv(1000000).decode()
        x_test = np.append(x_test, json.loads(batch),  axis = 0)
        clientsocket.send('OK'.encode())

    x_test = np.expand_dims(x_test, -1)
    print(np.array(x_test).shape)

    # y_test
    # -----------------------------------------

    print('========================')
    print('Receiving Testing Lables')
    print('========================')

    batch = clientsocket.recv(1000000).decode()
    y_test = json.loads(batch)
    clientsocket.send('OK'.encode())
    #print(np.array(facts1).shape)

    for i in tqdm(range(10,1000,10)):
        batch = clientsocket.recv(1000000).decode()
        y_test = np.append(y_test, json.loads(batch),  axis = 0)
        clientsocket.send('OK'.encode())

    #y_train = np.expand_dims(y_train, -1)
    print(np.array(y_test).shape)

    # ------------------- end of Data Import

    # model / data parameters
    num_classes = 10
    input_shape = (28, 28, 1)

    # scale images to range [0, 1]
    x_train = x_train.astype("float32") / 255
    x_test = x_test.astype("float32") / 255

    # make sure images have shape (28, 28, 1)
    #x_train = np.expand_dims(x_train, -1)
    #x_test = np.expand_dims(x_test, -1)
    print("x_train shape:", x_train.shape)
    print(x_train.shape[0], "train samples")
    print(x_test.shape[0], "test samples")

    # convert class vectors to binary class matrices
    y_train = keras.utils.to_categorical(y_train, num_classes)
    y_test = keras.utils.to_categorical(y_test, num_classes)

    # model

    model = keras.Sequential(
        [
            keras.Input(shape=input_shape),
            layers.Conv2D(32, kernel_size=(3, 3), activation="relu"),
            layers.MaxPooling2D(pool_size=(2, 2)),
            layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
            layers.MaxPooling2D(pool_size=(2, 2)),
            layers.Flatten(),
            layers.Dropout(0.5),
            layers.Dense(num_classes, activation="softmax"),
        ]
    )

    model.summary()

    # parameters for training
    batch_size = 128
    epochs = 3 # use epochs = 5

    model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

    model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, validation_split=0.1)

    # testing or evaluation
    score = model.evaluate(x_test, y_test, verbose=0)
    #model.save_weights('my_checkpoint')
    print("Test loss:", score[0])
    print("Test accuracy:", score[1])
    #print(weights)

    weights = model.get_weights()

    print('Disconnecting from client!')
    # print()
    print()


while True:

    # wait until a client connects
    (clientsocket, address) = serversocket.accept() #--> returns (clientsocket, address)
    # call the "handle_new_client" function to interact with the client
    handle_new_client(clientsocket,address)
    clientsocket.close()    # close the connection and start the next iteration of the loop to wait for the next client


print('The server is going down!')
serversocket.close()    # close down the server


