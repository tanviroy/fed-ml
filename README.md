# CS1340: Course Project
## Soham De, Tanvi Roy
------------------------

This is an implementation of suggested prompt 2 (as follows):

> Implementing your favourite Machine Learning training over LAN (client provides data,
learning happens at server)

In our case, we are training a simple CNN on MNIST dataset. The CNN architecture used is:

```
_________________________________________________________________
 Layer (type)                Output Shape              Param #   
=================================================================
 conv2d (Conv2D)             (None, 26, 26, 32)        320       
                                                                 
 max_pooling2d (MaxPooling2D  (None, 13, 13, 32)       0         
 )                                                               
                                                                 
 conv2d_1 (Conv2D)           (None, 11, 11, 64)        18496     
                                                                 
 max_pooling2d_1 (MaxPooling  (None, 5, 5, 64)         0         
 2D)                                                             
                                                                 
 flatten (Flatten)           (None, 1600)              0         
                                                                 
 dropout (Dropout)           (None, 1600)              0         
                                                                 
 dense (Dense)               (None, 10)                16010     
                                                                 
=================================================================
Total params: 34,826
Trainable params: 34,826
Non-trainable params: 0
_________________________________________________________________
```

For testing, we are only using 10000 samples from the original MNIST (60000 samples), but this framework can natively support datasets of any size. 

To run, open 2 tabs and run the following (in sequence)
```
python3 server.py
```
```
python3 client.py
```







