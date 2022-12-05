#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
client.py

Created on Mon Dec  5 16:05:35 2022

@author: charles
"""

import pyDes

from socket import *

serverName = "localhost"
serverPort = 12010
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

secret = b"This data is encrypted."
oraculo = pyDes.des("DESCRYPT", pyDes.CBC, b"\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)
enc_secret = oraculo.encrypt(secret)

print("Secret string: ", secret)
print("Encrypted secret: ", enc_secret)

clientSocket.send(enc_secret)
received = clientSocket.recv(1024)

print("From TCP Server encrypted:", received)
print("From TCP Server decrypted:", oraculo.decrypt(received))

clientSocket.close()