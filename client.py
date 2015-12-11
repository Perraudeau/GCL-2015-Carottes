#!/usr/bin/env python


LOG_FILE = '/root/youlogfile.log'  # path where messages send in udp are stored
HOST, PORT = "0.0.0.0", 514 # we define host and portto listen udp log messages
i = 0 #counter to determine first message sent by the injection server

import logging, SocketServer, zmq, signal
from threading import Timer

#we specify type of log, timestamp format of the log and where will be stored messages
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%b  %-d %H:%M:%S', filename=LOG_FILE, filemode='w')

#Class of our "syslog UDP server"
class SyslogUDPHandler(SocketServer.BaseRequestHandler):

        def handle(self):
                socket = self.request[1]
                print( "%s : " % self.client_address[0], str(self.request[0].strip())) #just to see messages in real time
                logging.info(self.request[0].strip()) # we log each raw message send by the server
                if return_i() == 0: #if first message
                        incremente_i() #we increment global var
                        signal.signal(signal.SIGALRM, conn) #we add a signal to send 
                        signal.alarm(240) #after 240 seconds we call conn() function
						
# this function is use to send messages stored in our local log file
def conn(signum,frame):
        f = open(LOG_FILE,"r+") #we open the file
        data = f.read() #we get all data content in a var
        context = zmq.Context() # we use zmq to open a socket
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://51.255.62.19:15555")
        socket.send(data) # we send our socket with the data (all log messages)
        socket.close()
        print("data send!")
        open(LOG_FILE,'w').close() # we empty our local log files
        decremente_i()

def incremente_i():
        global i
        i = 1

def return_i():
        global i
        return i

def decremente_i():
        global i
        i = 0

if __name__ == "__main__":
        try:
                server = SocketServer.UDPServer((HOST,PORT), SyslogUDPHandler) # start udp server to log messages
                server.serve_forever(poll_interval=0.5)
        except (IOError, SystemExit):
                raise
        except KeyboardInterrupt:
                print ("Crtl+C Pressed. Shutting down.")
