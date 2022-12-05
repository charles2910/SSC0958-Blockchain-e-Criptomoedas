#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
client_sig.py

Created on Mon Dec  5 16:05:35 2022

@author: charles
"""

import pickle


from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from socket import socket, AF_INET, SOCK_STREAM

serverName = "localhost"
serverPort = 12012
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

# load key
with open("/tmp/pem", "rb") as key_file:
    bytes_read = key_file.read()
    private_key = serialization.load_pem_private_key(
        bytes_read,
        password=None,
        )

transaction = {
    "Data": {
        "Sender": "Alice",
        "Receiver": "Bob",
        "Value": 10
    },
    "Signature": ""
}

transaction["Signature"] = private_key.sign(
    pickle.dumps(transaction['Data']),
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)

message = pickle.dumps(transaction)

pk = private_key.public_key()

pk.verify(
    transaction["Signature"],
    pickle.dumps(transaction['Data']),
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)

clientSocket.send(message)
received = clientSocket.recv(1024)

print("From TCP Server encrypted:", received.decode("utf-8"))

clientSocket.close()
