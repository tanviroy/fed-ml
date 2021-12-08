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

# wait for intro message
print(clientsocket.recv(1024).decode())   # --> returns a string

# send back an OK response to proceed with the sequence
clientsocket.send('OK'.encode())


# x_train
# -----------------------------------------
batch = clientsocket.recv(1000000).decode()
x_train = json.loads(batch)
clientsocket.send('OK'.encode())
#print(np.array(facts1).shape)

for i in tqdm(range(10,1000,10)):

    batch = clientsocket.recv(1000000).decode()
    x_train = np.append(x_train, json.loads(batch),  axis = 0)
    clientsocket.send('OK'.encode())

x_train = np.expand_dims(x_train, -1)
print(np.array(x_train).shape)

# y_train
# -----------------------------------------
batch = clientsocket.recv(1000000).decode()
y_train = json.loads(batch)
clientsocket.send('OK'.encode())
#print(np.array(facts1).shape)

for i in tqdm(range(10,1000,10)):
    batch = clientsocket.recv(1000000).decode()
    y_train = np.append(y_train, json.loads(batch),  axis = 0)
    clientsocket.send('OK'.encode())

#y_train = np.expand_dims(y_train, -1)
print(np.array(y_train).shape)


# x_test
# -----------------------------------------
batch = clientsocket.recv(1000000).decode()
x_test = json.loads(batch)
clientsocket.send('OK'.encode())
#print(np.array(facts1).shape)

for i in tqdm(range(10,100,10)):
    batch = clientsocket.recv(1000000).decode()
    x_test = np.append(x_test, json.loads(batch),  axis = 0)
    clientsocket.send('OK'.encode())

x_test = np.expand_dims(x_test, -1)
print(np.array(x_test).shape)

# y_test
# -----------------------------------------
batch = clientsocket.recv(1000000).decode()
y_test = json.loads(batch)
clientsocket.send('OK'.encode())
#print(np.array(facts1).shape)

for i in tqdm(range(10,100,10)):
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
epochs = 1 #use epochs = 5

model.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])

model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, validation_split=0.1)

# testing or evaluation
score = model.evaluate(x_test, y_test, verbose=0)
#model.save_weights('my_checkpoint')
print("Test loss:", score[0])
print("Test accuracy:", score[1])
#print(weights)

weights = model.get_weights()



for i in tqdm(range(0,6)):
    
    if i == 4 or i == 2:
        print("Avoid below")
        #for j in range() 
        print(type(weights[i]))
        print(weights[i].shape)
        if i == 2:
            print(sys.getsizeof(weights[i]))
        else:
            print(sys.getsizeof(weights[i][0:100]))
    else:
        print("Transmit below")
        print(type(weights[i]))
        print(weights[i].shape)
        print(sys.getsizeof(weights[i]))
        data = json.dumps(weights[i].tolist())
        clientsocket.recv(1024).decode()
        clientsocket.send(data.encode())


model2 = keras.Sequential(
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
model2.compile(loss="categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
model2.set_weights(weights)
model2.evaluate(x_test, y_test, verbose=0)
print("Test loss:", score[0])
print("Test accuracy:", score[1])



