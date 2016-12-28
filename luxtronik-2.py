#!/usr/bin/env python

import sys
import socket
import struct
import logging 

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s: %(levelname)-8s - %(message)s')
logger = logging.getLogger('Luxtronik2 Gateway')


class Luxtronic2:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.parameters = []
        self.calculated = []
        self.visibility = []

    def connect(self):
        try:
            self.hp = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
            self.hp.connect((self.host, self.port))
        except Exception as e:
            logger.critical("Error: connection failed {}".format(e))
            sys.exit(1)
        logger.info("Connected to Heatpump")

    def set_parameter(self, number, value):
        """ Command 3002 set parameter """
        return
        
        request = struct.pack('!iii', 3002, number, value)
        self.hp.send(request)
        data = self.hp.recv(4)
        response = struct.unpack('!i', data)
        if response[0] != 3002:
            logger.error("Error in 3002, invalid response")
            return
        data = self.hp.recv(4)
        response = struct.unpack('!i', data)
        if response[0] != value:
            logger.error("Error in 3002, invalid response")
            return
        logger.info("Sucessfully wrote parameter {} to value {}".format(number, value))

    def get_parameters(self):
        """ Command 3003 get parameters """
        
        request = struct.pack('!ii', 3003, 0)
        self.hp.send(request)
        data = self.hp.recv(4)
        response = struct.unpack('!i', data)
        if response[0] != 3003:
            logger.error("Error in 3003, invalid response")
            return
        data = self.hp.recv(4)
        response = struct.unpack('!i', data)
        for i in range(0, response[0]):
            data = self.hp.recv(4)
            self.parameters.append(struct.unpack('!i',data)[0])
        logger.info("Sucessfully read {} parameters".format(response[0]))

    def get_calculated(self):
        """ Command 3004 get parameters """
        
        request = struct.pack('!ii', 3004, 0)
        self.hp.send(request)
        data = self.hp.recv(4)
        response = struct.unpack('!i', data)
        if response[0] != 3004:
            logger.error("Error in 3004, invalid response")
            return
        data = self.hp.recv(4)
        status = struct.unpack('!i', data)[0]
        data = self.hp.recv(4)
        length = struct.unpack('!i', data)[0]
        for i in range(0, length):
            data = self.hp.recv(4)
            self.calculated.append(struct.unpack('!i',data)[0])
        logger.info("Sucessfully read {} calculations with status {}".format(length, status))

    def get_visibility(self):
        """ Command 3005 get visibility """
        
        request = struct.pack('!ii', 3005, 0)
        self.hp.send(request)
        data = self.hp.recv(4)
        response = struct.unpack('!i', data)
        if response[0] != 3005:
            logger.error("Error in 3005, invalid response")
            return
        data = self.hp.recv(4)
        response = struct.unpack('!i', data)
        for i in range(0, response[0]):
            data = self.hp.recv(1)
            self.visibility.append(struct.unpack('!b',data)[0])
        logger.info("Sucessfully read {} visibilitys".format(response[0]))

    def dump(self):
        logger.info("-"*30)
        logger.info("3003 : Parameters")
        logger.info("-"*30)
        for i,e in enumerate(self.parameters):
            logger.info("{} : {}".format(i,e))
        logger.info("-"*30)
        logger.info("3004 : Calculations")
        logger.info("-"*30)
        for i,e in enumerate(self.calculated):
            logger.info("{} : {}".format(i,e))
        logger.info("-"*30)
        logger.info("3005 : Visibilitys")
        logger.info("-"*30)
        for i,e in enumerate(self.visibility):
            logger.info("{} : {}".format(i,e))

if __name__ == "__main__":
    lt = Luxtronic2('192.168.88.11',8889)
    lt.connect()
    lt.get_parameters()
    lt.get_calculated()
    lt.get_visibility()
    lt.dump()
