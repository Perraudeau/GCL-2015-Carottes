#!/bin/usr/env python

import zmq, signal
#our udp socket server to receive sockets from the client
def conn():
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.bind("tcp://*:15555") # we listen on the 15555 port in background
        message = socket.recv() # if we receive a socket (eg. all logs messages)
        writer(message) # we write messages in a file
        signal.signal(signal.SIGALRM,vide)
        signal.alarm(300) # after 300 seconds we empty the gclc.log => because no messages were sent by the client

def writer(data):
        f = open('/opt/gclc/gclc.log','w')
        f.write(data)
        f.close()

def vide(signum,frame):
        open('/opt/gclc/gclc.log','w').close()

if __name__ == "__main__":
        try:
                while 1:
                        conn()
        except (IOError, SystemExit):
                raise
        except KeyboardInterrupt:
                print ("Crtl+C Pressed. Shutting down.")
