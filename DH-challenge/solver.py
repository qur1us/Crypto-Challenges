from Crypto.Cipher import AES
import argparse
import pbkdf2
import json
from base64 import b64decode


def decrypt(json_input, shared_secret: int) -> str:
    key = pbkdf2.PBKDF2(str(shared_secret), b"S3cR37_s4l7").read(32)
    b64 = json.loads(json_input)
    json_k = [ 'nonce', 'ciphertext', 'tag' ]
    jv = {k:b64decode(b64[k]) for k in json_k}
    cipher = AES.new(key, AES.MODE_GCM, nonce=jv['nonce'])
    plaintext = cipher.decrypt_and_verify(jv['ciphertext'], jv['tag'])
    return plaintext.decode('utf-8')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='DH_challenge_solver', description='Solves DH challenge created fro VUT CyberRange. Created by team of handsome OSCP owners.')
    parser.add_argument('json')
    parser.add_argument('-s', '--shared-secret', default=1)
    args = parser.parse_args()
    
    try:
        flag = decrypt(args.json, args.shared_secret)
    except:
        print("Decryption or verification of the message failed!")
        exit()

    print(flag)
