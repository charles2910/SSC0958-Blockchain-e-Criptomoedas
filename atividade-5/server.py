#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
server.py

Created on Mon Dec  5 16:02:36 2022

@author: charles
"""

import pyDes

from socket import *

serverPort = 12010
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.bind(('0.0.0.0',serverPort))
serverSocket.listen(1)

oraculo = pyDes.des("DESCRYPT", pyDes.CBC, b"\0\0\0\0\0\0\0\0", pad=None, padmode=pyDes.PAD_PKCS5)

print('The server is ready to receive')

while 1:
     connectionSocket, addr = serverSocket.accept()

     sentence = connectionSocket.recv(1024)


     print("TCP Received", sentence, "FROM", addr)
     print("Encrypted secret: ", sentence)

     decryptedSentence = oraculo.decrypt(sentence)

     print("Decrypted secret: ", decryptedSentence)

     decryptedSentence += b" Only if you don't have the key!"
     encryptedSentence = oraculo.encrypt(decryptedSentence)

     connectionSocket.send(encryptedSentence)
     connectionSocket.close()