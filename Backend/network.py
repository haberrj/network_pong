#!/usr/bin/python3

# Author: Ron Haber
# Date: 22.5.2021
# A class for connecting to the network.

import socket
import pickle

class Network:
    def __init__(self, server_ip, server_port):
        '''The constructor for the class to connect the client to the
        server.
        @param server_ip: A string representing the IP address of the server.
        @param server_port: An integer representing the Port Number of the server.
        '''
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_ip = server_ip
        self.port_num = server_port
        self.address = (self.server_ip, self.port_num)
        self.p = self.connect()

    def connect(self):
        '''Will connect/receive data to/from the server.
        '''
        try:
            self.client.connect(self.address)
            return pickle.loads(self.client.recv(2048))
        except:
            pass
    
    def getP(self):
        return self.p
    
    def send(self, data):
        '''Will send a message via the network based on the data provided.
        @param data: A list or tuple to be sent over the network.
        '''
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)
        
