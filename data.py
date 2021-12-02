# import libraries 
import numpy as np
#import json
from pickle import dumps, loads

# splitting data into train and test sets
#(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()
with np.load('mnist.npz', allow_pickle=True) as f:
    x_train, y_train = f['x_train'], f['y_train']
    x_test, y_test = f['x_test'], f['y_test']

print(y_train[0:1000])
# scale images to range [0, 1]
x_train = x_train.astype("float32") / 255
x_test = x_test.astype("float32") / 255

# make sure images have shape (28, 28, 1)
x_train = np.expand_dims(x_train, -1)
x_test = np.expand_dims(x_test, -1)

print("x_train shape:", x_train.shape)
print(type(x_train))
x_train_str = dumps(x_train)
print(type(x_train_str))
print(len(x_train_str))
x_train_rec = loads(x_train_str)
print(type(x_train_rec))
print("x_train_rec shape:", x_train_rec.shape)

print(x_train.shape[0], "train samples")
print(x_test.shape[0], "test samples")