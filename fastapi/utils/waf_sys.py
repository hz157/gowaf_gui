'''
Descripttion: 
version: 
Author: Ryan Zhang (gitHub.com/hz157)
Date: 2024-04-13 20:56:35
LastEditors: Ryan Zhang
LastEditTime: 2024-04-13 20:57:54
'''
import socket

def CheckPortUse(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0