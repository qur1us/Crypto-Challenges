import gmpy2
from Crypto.Util.number import long_to_bytes
import argparse, socket, re

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
    
    def recvall(self):
        # Helper function to recv data until 'Closing channel.' message
        data = bytearray()
        while not data.decode().endswith("Closing channel."):
            packet = self.sock.recv(4096)
            if packet == b'':
                continue;
            print(packet.decode())
            data.extend(packet)
        return data.decode()

class Attack:
    #https://github.com/HexPandaa/RSA-Common-Modulus-Attack
    def __init__(self):
        self.a = 0
        self.b = 0
        self.m = 0
        self.i = 0

    def gcd(self, num1, num2):
        """
        This function os used to find the GCD of 2 numbers.
        :param num1:
        :param num2:
        :return:
        """
        if num1 < num2:
            num1, num2 = num2, num1
        while num2 != 0:
            num1, num2 = num2, num1 % num2
        return num1

    def extended_euclidean(self, e1, e2):
        """
        The value a is the modular multiplicative inverse of e1 and e2.
        b is calculated from the eqn: (e1*a) + (e2*b) = gcd(e1, e2)
        :param e1: exponent 1
        :param e2: exponent 2
        """
        self.a = gmpy2.invert(e1, e2)
        self.b = (float(self.gcd(e1, e2)-(self.a*e1)))/float(e2)

    def modular_inverse(self, c1, c2, N):
        """
        i is the modular multiplicative inverse of c2 and N.
        i^-b is equal to c2^b. So if the value of b is -ve, we
        have to find out i and then do i^-b.
        Final plain text is given by m = (c1^a) * (i^-b) %N
        :param c1: cipher text 1
        :param c2: cipher text 2
        :param N: Modulus
        """
        i = gmpy2.invert(c2, N)
        mx = pow(c1, self.a, N)
        my = pow(i, int(-self.b), N)
        self.m= mx * my % N

    def print_flag(self):
        print("\n\nFlag: ", long_to_bytes(self.m).decode())

def hex2int(string):
    return int(string.split(': ')[1], 16)
    

def main():
    parser = argparse.ArgumentParser(prog='RSA_challenge_solver', description='Solves RSA challenge created for VUT CyberRange. Developed by team of OSCP owners.')
    parser.add_argument('-i', '--ip', dest='ip', required=True, type=str)
    parser.add_argument('-p', '--port', dest='port', required=True, type=int)
    args = parser.parse_args()
    
    s = TCPConnection()
    s.connect(args.ip, args.port)
    
    data = s.recvall()
    
    n = re.search(r"n: .*", data)
    n = hex2int(n[0])
    
    e1 = re.search(r"Alice's Public Key: .*", data)
    e1 = hex2int(e1[0])
    
    e2 = re.search(r"Bob's Public Key: .*", data)
    e2 = hex2int(e2[0])
    
    c1 = re.search(r"Alice's encrypted flag: .*", data)
    c1 = hex2int(c1[0])
    
    c2 = re.search(r"Bob's encrypted flag: .*", data)
    c2 = hex2int(c2[0])
    
    a = Attack()
    a.extended_euclidean(e1, e2)
    a.modular_inverse(c1, c2, n)
    a.print_flag()

if __name__ == '__main__':
    main()