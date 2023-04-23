#!/usr/bin/python3
import sys
import hashlib

# INPLEMENTING THIS CUSTOM FUNCTION TO CRACK THE HASHES
#
# const salt = "za1&P^tMvkvz#Xe%7B4j"
#       
# let hash = password
#
# for (let i = 0; i <= 1337; i++) {
#     hash = crypto.createHash("md5").update(hash + salt).digest("hex");
# }
#     
# return hash


def main():
    hash_file = sys.argv[1]
    wordlist = sys.argv[2]

    salt = "za1&P^tMvkvz#Xe%7B4j"

    with open(hash_file, 'r') as h:
        lines = h.readlines()
        
        for line in lines:
            line = line[:-1]
            cracked = False

            print(f"Cracking {line}")

            with open(wordlist, 'rb') as w:
                passwords = w.readlines()
                
                for password in passwords:
                    password = password[:-1]
                    sys.stdout.write(f"\r{password.decode('utf-8')}")
                    sys.stdout.flush()
                    
                    h_password = password.decode('utf-8')

                    for i in range(1338):
                        h_password = hashlib.md5((h_password + salt).encode('utf-8')).hexdigest()

                    if h_password == line:
                        print(f"\r[+] Hash cracked: {password.decode('utf-8')}\n")
                        cracked = True
                        break
            
            if not cracked:
                print("\r[-] Failed to crack.\n")


if __name__ == '__main__':
    main()
