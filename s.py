import socket
import json
import numpy as np

# instantiate server's socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# define address params
IP = '127.0.0.1'
PORT = 5001

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


random_facts = np.array([
    [['The national dish of the UK is Chicken Tikka Masala'], ['The whole of Britain']],
    [['Some cats are allergic to humans'], ['Anonymous']]
]).tolist()


'''

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

    for i in range(10,1000,10):
    	batch = x_train[i:i+10].tolist()
    	data = json.dumps(batch)
    	clientsocket.send(data.encode())
    	print(clientsocket.recv(1024).decode())

    # y_train
    # --------------------------------------
    batch = y_train[0:10].tolist()
    data = json.dumps(batch)
    clientsocket.send(data.encode())
    print(clientsocket.recv(1024).decode())

    for i in range(10,1000,10):
    	batch = y_train[i:i+10].tolist()
    	data = json.dumps(batch)
    	clientsocket.send(data.encode())
    	print(clientsocket.recv(1024).decode())


    # x_test
    # --------------------------------------
    batch = x_test[0:10].tolist()
    data = json.dumps(batch)
    clientsocket.send(data.encode())
    print(clientsocket.recv(1024).decode())

    for i in range(10,100,10):
    	batch = x_test[i:i+10].tolist()
    	data = json.dumps(batch)
    	clientsocket.send(data.encode())
    	print(clientsocket.recv(1024).decode())

    # y_test
    # --------------------------------------
    batch = y_test[0:10].tolist()
    data = json.dumps(batch)
    clientsocket.send(data.encode())
    print(clientsocket.recv(1024).decode())

    for i in range(10,100,10):
    	batch = y_test[i:i+10].tolist()
    	data = json.dumps(batch)
    	clientsocket.send(data.encode())
    	print(clientsocket.recv(1024).decode())


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


