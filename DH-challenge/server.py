from Crypto.Cipher import AES
from Crypto.Util.number import getPrime
import random
import socketserver
import signal
import os
import pbkdf2
from base64 import b64encode
import json


FLAG = b"FLAG{SuP3r_S3cRe7_fL4g_f0R_T3s71nG}"
p = getPrime(2048)
g = 7


class Handler(socketserver.BaseRequestHandler):
    def handle(self):
        signal.alarm(0)
        main(self.request)


class ReusableTCPServer(socketserver.ForkingMixIn, socketserver.TCPServer):
    pass


def sendMessage(s, msg):
    s.send(msg.encode())


def recieveMessage(s, msg):
    sendMessage(s, msg)
    return s.recv(4096).decode().strip()

def encrypt(message, shared_secret):
    # https://pycryptodome.readthedocs.io/en/latest/src/cipher/modern.html#gcm-mode
    key = pbkdf2.PBKDF2(str(shared_secret), b"S3cR37_s4l7").read(32)
    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(message)
    json_k = [ 'nonce', 'ciphertext', 'tag' ]
    json_v = [ b64encode(x).decode('utf-8') for x in (cipher.nonce, ciphertext, tag) ]
    result = json.dumps(dict(zip(json_k, json_v)))
    return result


def main(s):
    a = random.randrange(2, p - 1)
    A = pow(g, a, p)

    sendMessage(s, "Generating DH Parameters...\n")
    sendMessage(s, f"g = {g}, p = {p}\n\n")
    sendMessage(s, "Set-up Sequence Complete!\n\n")

    sendMessage(s, "Generating the Public Key...\n")

    sendMessage(s, "Calculation Completed!\n")
    sendMessage(s, "Public Key is: ???\n\n")

    B = recieveMessage(s, "Enter Your Public Key: ")
    print("[*] Public Key received")

    try:
        B = int(B)
    except:
        sendMessage(s, f"Can't convert {B} to INT\n")
        exit()

    sendMessage(s, "\n" + "Calculating The Shared Secret\n")
    shared_secret = pow(B, a, p)
    print(f"[*] Shared secret: {shared_secret}")
    sendMessage(s, "Calculation Complete\n\n")

    sendMessage(s, "Encrypting Flag with shared_secret...\n")
    result = encrypt(FLAG, shared_secret)
    sendMessage(s, f"Here is The Encrypted Flag: {result}\n")
    print("[*] Sending Flag")
    sendMessage(s, "Closing Channel...\n\n")
    exit()


if __name__ == '__main__':
    socketserver.TCPServer.allow_reuse_address = True
    server = ReusableTCPServer(("0.0.0.0", 1337), Handler)
    print("[*] Server started!")
    server.serve_forever()
