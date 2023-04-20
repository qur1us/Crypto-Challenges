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

    def readline(self):
        data = self.sock.recv(1024).decode()
        return data
        
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

    s = TCPConnection()
    s.connect(args.ip, args.port)
    data = s.readline()
    data += s.readline()
    data += s.readline()
    data += s.readline()
    s.send(b'1')
    data += s.readline()
    data += s.readline()
    data += s.readline()
    data += s.readline()
    print(data)
    
    #https://stackoverflow.com/questions/34959948/parse-valid-json-object-or-array-from-a-string
    json_str = re.findall(r"{.+[:,].+}|\[.+[,:].+\]", data)[0]
	
    try:
        flag = decrypt(json_str, 1)
    except:
        print("Decryption or verification of the message failed!")
        exit()

    print(f"The flag is: {flag}")
