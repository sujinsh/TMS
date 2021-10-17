# """
# Multi-threaded TCP Server
# Multithreaded Server.py acts as a standard TCP server, with multi-threaded integration, spawning a new thread for each
# client request it receives.
# This is derived from an assignment for the Distributed Systems class at Bennington College
# """
from argparse import ArgumentParser
from threading import Lock, Thread
from socket import SO_REUSEADDR, SOCK_STREAM, socket, SOL_SOCKET, AF_INET
import time
from Filters import MeanFilter, WeightedFilter, ConstFilter
import numpy as np
import struct

class ClientHandler(Thread):
    def __init__(self, address, port, socket, lock, filter):
        Thread.__init__(self)
        self.address = address
        self.port = port
        self.socket = socket
        self.lock = lock
        self.filter = filter
        self.Flag = True

    def stop(self):
        self.Flag = False

    def run(self):
        try:
            while self.Flag:
                time.sleep(0.1)
                point = self.filter.get()
                if point is None:
                    continue
                message = ""
                for p in point:
                    message += str(p) + ","
                print("send:", message)
                self.socket.send(struct.pack("@i", len(message)))
                self.socket.send(message.encode(encoding="ascii"))
                # self.socket.send("done".encode())
        except ConnectionError as e:
            print(e)
        self.socket.close()


class TCPServer(Thread):

    def __init__(self, ip="localhost", port=9000):
        Thread.__init__(self)
        self.revcQueue = []
        self.revcQueueLock = Lock()
        self.ip = ip
        self.port = port
        self.filter = ConstFilter()
        self.Flag = True

    def stop(self):
        self.Flag = False
        self.s.close()

    def addPoint(self, point):
        self.filter.add(point)

    def run(self):

        # Initialize instance of an argument parser
        parser = ArgumentParser(description='Multi-threaded TCP Server')
        # Add optional argument, with given default values if user gives no arg
        parser.add_argument('-p', '--port', default=self.port, type=int, help='Port over which to connect')
        # Get the arguments
        args = parser.parse_args()
        thread_lock = Lock()

        self.s = socket(AF_INET, SOCK_STREAM)
        self.s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.s.bind((self.ip, args.port))
        # Create a list in which threads will be stored in order to be joined later
        threads = []
        # Continuously listen for a client request and spawn a new thread to handle every request
        print("start server...")
        try:
            while self.Flag:
                self.s.listen(2)
                sock, addr = self.s.accept()
                print("connected!")
                # Spawn a new thread for the given request
                newThread = ClientHandler(addr[0], addr[1], sock, thread_lock, self.filter)
                newThread.start()
                threads.append(newThread)

        except Exception as e:
            print(e)
            print("\nExiting Server\n")

        # When server ends gracefully (through user keyboard interrupt), wait until remaining threads finish
        for item in threads:
            item.stop()
            item.join()

if __name__ == "__main__":
    ss = TCPServer()
    ss.start()
    ss.addPoint(np.array([0, 0, 1, 0, 0,0]))
    time.sleep(5)
    ss.addPoint(np.array([0, 0, 1, 0, 0, 0]))
    time.sleep(1)
    for i in range(500):
        time.sleep(0.1)
        ss.addPoint(np.array([0.6853,0.221,-0.03238,-2.717,-0.273,-3.1415]))
    ss.stop()
    print("stop")

# import threading
# import time
# from socket import SO_REUSEADDR, SOCK_STREAM, SOL_SOCKET, AF_INET, socket
# from Filters import MeanFilter, WeightedFilter
#
#
# class TCPServer(threading.Thread):
#     """
#     单线程接受数据
#     """
#
#     def __init__(self, ip="localhost", port=9000):
#         """
#         :param ip: tcp ip
#         :param port: tcp 端口
#         """
#         threading.Thread.__init__(self)
#         # self.filter = WeightedFilter(0.80)
#         self.tcp_ip = ip
#         self.tcp_port = port
#         self.Flag = True
#         self.canrun = False
#         self.socket = socket(AF_INET, SOCK_STREAM)
#         self.socket.bind((self.tcp_ip, self.tcp_port))
#         self.socket.listen()
#         self.message = None
#         self.point = None
#         self.connect, self.addr = self.socket.accept()
#
#     def addPoint(self, point):
#         self.point = point
#
#     def pos(self):
#         return self.point
#
#     def stop(self):
#         self.socket.close()
#         self.Flag = False
#         print("\nStop Listen and Exit Tcp Server")
#
#     def run(self):
#         try:
#             # self.socket.connect((self.tcp_ip, self.tcp_port))
#             while self.Flag:
#                 if self.canrun:
#                     if self.point is None or not any(self.point):
#                         continue
#                     else:
#                         self.message = ""
#                         for p in self.point:
#                             self.message += str(p) + ','
#                         print(self.message)
#                         data = self.message.encode()
#                         self.connect.send(data)
#                         time.sleep(0.1)
#         except ConnectionError as e:
#             print("TCP connect Error")
#             print(e)
#             self.socket.close()

#
# if __name__ == "__main__":
#     ss = TCPServer()
#     ss.start()
#     # time.sleep(5)
#     # ss.addPoint(np.array([0, 0, 1]))
#     # time.sleep(1)
#     ss.canrun= True
#     paths = [
#         [0.497361, -0.014441, 0.158609, 3.006, -0.122, 2.364],
#         [0.638344, -0.014443, 0.158613, 3.006, -0.122, 2.364],
#         [0.563928, 0.030541, 0.233577, -3.051, -0.131, 2.246]
#     ]
#     i = 1
#     while 1:
#         # time.sleep(1)
#         ss.addPoint(paths[i % 3])
#         print(paths[i % 3])
#         i += 1
#     ss.stop()
#     print("stop")
