from Crypto.Cipher import AES
import argparse, pbkdf2, json, socket, re
from base64 import b64decode

class TCPConnection:
    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        try:
            self.sock.connect((host, port))
            #print('Successful Connection')
        except:
            print('Connection Failed')
    
    def recvuntil(self, message):
        # Helper function to recv data until 'Closing channel.' message
        data = bytearray()
        while not data.decode().endswith(message):
            packet = self.sock.recv(4096)
            if packet == b'':
                continue;
            print(packet.decode())
            data.extend(packet)
        return data.decode()
        
    def send(self, data):
        self.sock.sendall(data)

def decrypt(json_input, shared_secret: int) -> str:
	key = pbkdf2.PBKDF2(str(shared_secret), b"S3cR37_s4l7").read(32)
	b64 = json.loads(json_input)
	json_k = [ 'nonce', 'ciphertext', 'tag' ]
	jv = {k:b64decode(b64[k]) for k in json_k}
	cipher = AES.new(key, AES.MODE_GCM, nonce=jv['nonce'])
	plaintext = cipher.decrypt_and_verify(jv['ciphertext'], jv['tag'])
	return plaintext.decode('utf-8')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='DH_challenge_solver', description='Solves DH challenge created for VUT CyberRange. Developed by team of OSCP owners.')
    parser.add_argument('-i', '--ip', dest='ip', required=True, type=str)
    parser.add_argument('-p', '--port', dest='port', required=True, type=int)
    args = parser.parse_args()
    
    # Different solution approaches
    solution = 0
    #solution = 1

    s = TCPConnection()
    s.connect(args.ip, args.port)
    data = s.recvuntil("Enter Your Public Key: ")
    s.send(str(solution).encode())
    data += s.recvuntil("Closing Channel.")
    #print(data)
    
    #https://stackoverflow.com/questions/34959948/parse-valid-json-object-or-array-from-a-string
    json_str = re.findall(r"{.+[:,].+}|\[.+[,:].+\]", data)[0]
	
    try:
        flag = decrypt(json_str, solution)
    except:
        print("Decryption or verification of the message failed!")
        exit()

    print(f"\n\nThe flag is: {flag}")
