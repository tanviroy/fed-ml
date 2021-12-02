import socket
import json
import numpy as np
from pickle import dumps, loads

# instantiate server's socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# define address params
IP = '127.0.0.1'
PORT = 5545

# bind server
serversocket.bind( (IP, PORT) )

# start listening
serversocket.listen()


print('The server is up! Listening at:',IP,PORT)
print()




# ----------------- DATA -------------------

'''
Random Fact Hub!
Allows users to view random facts from our database, and add new facts to it
'''

random_facts = [
    ['The national dish of the UK is Chicken Tikka Masala', 'The whole of Britain'],
    ['Some cats are allergic to humans', 'Anonymous']
]

with np.load('mnist.npz', allow_pickle=True) as f:
    x_train = f['x_train']


view_count = 0
# every time a new user connects, we increase view count by 1

# ------------------------------------------

def handle_new_client(clientsocket, address):

    global random_facts
    global view_count
    global x_train

    print('-------------------------------------------')
    print('New connection made! Client address:',address)


    # interact with client
    # --------------------------------------------------------------

    # send intro message
    intro = 'Welcome to the Random Fact Hub!\n'

    clientsocket.send(intro.encode())

    # wait for OK response
    if clientsocket.recv(1024).decode() != 'OK':
        print('Something went wrong! Disconnecting')
        clientsocket.close()


    # send available facts
    # convert random_facts to a string

    #data = json.dumps(random_facts) # type(data) = string
    print("x_train shape:", x_train[0:20].shape)
    #print(type(x_train[0:10]))
    #print(len(data))
    data = dumps(x_train[0:10])
    print(len(data))

    # send data string to client
    #clientsocket.send(data.encode())
    clientsocket.send(data)

    for i in range(1,6):
        data = dumps(x_train[(i*10):(i*10)+10])
        #data = dumps(x_train[10:20])
        print(len(data))
        clientsocket.send(data)



    # wait to see if client wants to add a new fact
    choice = clientsocket.recv(1024).decode()   # either y/n

    if choice == 'n' or choice == 'N':
        # send outro message
        clientsocket.send('Thanks for connecting to the Random Fact Hub! :)\n'.encode())

    elif choice == 'y' or choice == 'Y':
        # ask client for fact
        clientsocket.send('Send us your fact!\n'.encode())
        # wait for response
        fact = clientsocket.recv(1024).decode()

        # ask client for signature
        clientsocket.send('Send in your name/signature!\n'.encode())
        # wait for response
        sign = clientsocket.recv(1024).decode()

        print('Adding a new fact to the database!')
        random_facts.append([fact,sign])


        # send OK response to client
        clientsocket.send('Thank you for your fact! It has been added to the database.'.encode())

    else:
        # send error message to client
        clientsocket.send('Invalid choice! Try again...'.encode())


    # -------------------------------------------------------------

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




'''
__________________________________________________________________________________________

Sequence of Events:

1. Client connects to server
2. Server accepts connection

(Interaction begins)

3. Server sends intro message
4. Client sends OK response
5. Server sends facts from database
6. Client sends choice (Y/N)
7(a). If choice = N, server sends outro message
7(b). If choice = Y, 
    (i). Server sends fact request
    (ii). Client sends fact
    (iii). Server sends signature request
    (iv). Client sends signature
    (v). Server sends OK response

7(c). If choice = invalid, server sends err message



Note:

You can only send string data across the sockets.
    socket.send('some string'.encode())

So make sure you convert data to string before sending, and convert it back after receiving.


Both the server and client must know the sequence of events.
For example, whenever the sequence involves the server sending a message, 
the client must try to receive it using
    socket.recv().decode()




Further changes and additions:

1. Processing data like IP address, user credentials, etc
2. Threading
3. Indefinite sequence of events
...




'''