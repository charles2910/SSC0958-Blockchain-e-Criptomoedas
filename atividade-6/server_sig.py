#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
server_sig.py

Created on Mon Dec  5 16:02:36 2022

@author: charles
"""

import pickle

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from socket import socket, AF_INET, SOCK_STREAM

serverPort = 12012
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('0.0.0.0', serverPort))
serverSocket.listen(1)

# load public key
with open("/tmp/pem.pub", "rb") as key_file:
    public_key = serialization.load_pem_public_key(key_file.read())

print('The server is ready to receive')

while 1:
    connectionSocket, addr = serverSocket.accept()

    message = connectionSocket.recv(1024)
    transaction = pickle.loads(message)

    try:
        public_key.verify(
            transaction["Signature"],
            pickle.dumps(transaction['Data']),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
    except InvalidSignature:
        print("Invalid signature")
        answer = b"Invalid Signature"
    else:
        answer = b"Valid Signature"

    print(answer.decode("utf-8"))
    connectionSocket.send(answer)
    connectionSocket.close()
