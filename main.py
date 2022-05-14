'''
    Port scan local host ports using socket
'''
import socket, threading, queue

# get IP address of your computer
hostname = socket.gethostname()
ipaddress = socket.gethostbyname(hostname)

# or use the local host address
target = '127.0.0.1' 

# a list to store all open ports 
open_ports = []
# create a queue for store all ports
port_queue = queue.Queue()
# create a list for storing threads for join() later
thread_list=[]

# method for doing port scanning
def port_scan(port):
    try:
        # create a 'client socket' using connect()
        # not a 'server socket' with 'bind' and 'listen'
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        sock.connect((ipaddress,port)) # connect to a tuple
        print(f'{port} is connected')
        open_ports.append(port)
    except:
        pass

# put all ports into a queue
def enqueue_ports():
    for i in range(0, 1024):
        port_queue.put(i)

# the task that needs to be done by each thread continuously
def worker():  
    # run continuously when queue is not empty
    while not port_queue.empty():
        # remove and get a port from the queue
        port_number = port_queue.get()
        # print(port_number)
        port_scan(port_number)
    

# 
def create_thread(num):  
    # create all threads  
    for _ in range(num):
        # must use 'target='
        thread = threading.Thread(target =worker)
        thread_list.append(thread) 
    # start all threads
    for thread in thread_list:
        thread.start()
    # wait till all threads to finish
    for thread in thread_list:
        thread.join()     

    print('All done!')      

def run_port_scanning():
    enqueue_ports()
    create_thread(500)
    print(open_ports)

run_port_scanning()

