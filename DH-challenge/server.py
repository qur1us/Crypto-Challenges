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
    sendMessage(s, "\nGenerating DH Parameters...")
    sendMessage(s, f"\ng = {g}, p = {p}")
    sendMessage(s, "\nGenerating the Public Key...")
    
    a = random.randrange(2, p - 1)
    A = pow(g, a, p)
    
    sendMessage(s, "\nCalculation Completed!")
    sendMessage(s, "\nPublic Key is: ???")

    B = recieveMessage(s, "\nEnter Your Public Key: ")
    print("[*] Public Key received")

    try:
        B = int(B)
    except:
        sendMessage(s, f"\nCan't convert {B} to INT")
        exit()

    sendMessage(s, "\nCalculating The Shared Secret")
    shared_secret = pow(B, a, p)
    print(f"[*] Shared secret: {shared_secret}")
    sendMessage(s, "\nCalculation Complete")

    sendMessage(s, "\nEncrypting Flag with shared_secret...")
    result = encrypt(FLAG, shared_secret)
    sendMessage(s, f"\nHere is The Encrypted Flag: {result}")
    print("[*] Sending Flag")
    sendMessage(s, "\nClosing Channel.")
    exit()


if __name__ == '__main__':
    socketserver.TCPServer.allow_reuse_address = True
    server = ReusableTCPServer(("0.0.0.0", 1337), Handler)
    print("[*] Server started!")
    server.serve_forever()
