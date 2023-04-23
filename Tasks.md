# Úkol 1

Tvým úkolem bude analyzovat zdrojový kód aplikace, identifikovat zranitelnost a následně tuto zranitelnost zneužít k získání vlajky.

## Nápovědy

**Požádat o nápovědu 1 (penalizace 25 %)**

Zaměř se na společné parametry obdržených zpráv.

**Požádat o nápovědu 2 (penalizace 50 %)**

Zkus vyhledat více informací k útoku na společný modulus (RSA common modulus attack).

**Požádat o nápovědu 3 (penalizace 75 %)**

Útok na společný modulus je vhodně popsán [zde](https://infosecwriteups.com/rsa-attacks-common-modulus-7bdb34f331a5#84d1).

**Požádat o nápovědu 4 (penalizace 100 %)**

`FLAG{N3veR_sH4r3_pr1m3S_w17h_y0uR_fR13nd5}`

# Úkol 2

Tvým úkolem bude analyzovat zdrojový kód aplikace, identifikovat zranitelnost a následně tuto zranitelnost zneužít k získání vlajky.

## Nápovědy

**Požádat o nápovědu 1 (penalizace 25 %)**

Zaměř se na to jakým způsobem aplikace vypočítá klíč $k$, kterým zašifruje text vlajky.

**Požádat o nápovědu 2 (penalizace 50 %)**

Zkus odeslat takové $B$, aby dohodnutý šifrovací klíč $k$ byl předvídatelný.

**Požádat o nápovědu 3 (penalizace 75 %)**

Zkus odeslat $B=1$.

**Požádat o nápovědu 4 (penalizace 100 %)**

`FLAG{N0th1n6_1S_tRu3_eV3ryTh1nG_i5_p3rM173D}`

# Úkol 3

Tvojou úlohou bude zanalyzovať zdrojový kód webovej aplikácie a pomocou získaných informácii sa pokúsiť cracknúť niekoľko uniknutých hashov užívateľov webovej aplikácie. Ak sa ti podarí nejaký z hashov cracknúť, môžeš sa do webovej aplikácie prihlásiť do jeho účtu.

## Nápovědy

**Požádat o nápovědu 1 (penalizace 25 %)**

Necrackovať pomocou software ako hashcat či john. Preskúmať akým spôsobom funguje hashovanie hesiel v  zdrojovom kóde. Je potrebné použiť a vhodným spôsobom upraviť funkciu starajúcu sa o hashovanie a ukladanie do databázy a prispôsobiť na slovníkový útok vo vlastnom skripte.

**Požádat o nápovědu 2 (penalizace 50 %)**

Pseudo kód pre implementáciu slovníkového útoku:

```python
open file:
	readhashes()

	for hash in hashes:
		open file:
			readwordlist()

			for password in wordlist:
				hashpassword()
				
				if original == hashed_password:
					cracked = True
```

**Požádat o nápovědu 3 (penalizace 75 %)**

```python
.
.
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
                    
                    h_password = hashlib.md5((password.decode('utf-8') + salt).encode('utf-8')).hexdigest()

                    for i in range(1337):
                        h_password = hashlib.md5((h_password + salt).encode('utf-8')).hexdigest()

                    if h_password == line:
                        print(f"\r[+] Hash cracked: {password.decode('utf-8')}\n")
                        cracked = True
                        break
            
            if not cracked:
                print("\r[-] Failed to crack.\n")
.
.
```

**Požádat o nápovědu 4 (penalizace 100 %)**

`FLAG{EVERY_HACKER_MUST_KNOW_SOME_JS}`

# Úkol 4

Získal/a jsi přístup k síťové aplikaci a jejímu zdrojovému kódu. Zdá se, že se jedná o jednoduchého správce hesel, který si administrátor sám napsal. Opravdu by se ti hodilo získat jeho hesla... Není možné se k jeho heslům skrze aplikaci nějak dostat? Ten zdrojový kód by se mohl hodit.

## Nápovědy

**Požádat o nápovědu 1 (penalizace 25 %)**

Prozkoumejte všechny funkcionality aplikace.

**Požádat o nápovědu 2 (penalizace 50 %)**

Využijte poskytnutý zdrojový kód aplikace a podívejte se, jak byly vytvořeny logovací záznamy (MENU volba 9).

**Požádat o nápovědu 3 (penalizace 75 %)**

Funkce generate_secure_filename loguje timestamp, který zároveň používá jako seed pro generování náhodného názvu souboru. Vyčtěte z logu aplikace timestamp "Random filename generated" příslušící uživateli admin. Zjištěné datum a čas převeďte na UNIX timestamp a s pomocí výsledné hodnoty znovu vytvořte název souboru uživatele admin a tento soubor následně z aplikace stáhněte.

**Požádat o nápovědu 4 (penalizace 100 %)**

`FLAG{kE3p_s3eD_sEcr37_K3eP_SE3d_5aF3}`


# Otázky

## 1. Jakým způsobem by bylo možné zranitelnost odstranit?

1. Zvýšit bitovou velikost generovaných prvočísel (`BITSIZE`) na hodnotu alespoň $8192$.
2. **Prvočísla generovat v rámci funkce `rsa_keygen()`, namísto `handleIncomingRequest()`**.
3. Přičtením veřejných klíčů ke společnému modulu.
4. Zavedením takového paddingu, aby šifrovaná zpráva přesahovala modulus.

## 2.Zranitelnost aplikace spočívá v:

1. Použití nedostatečně velkého prvočísla ($2048$ bitů).
2. Použití AES256-GCM z knihovny `Crypto.Cipher` pro `python` k šifrování vlajky.
3. **Absenci validace soukromých (a tedy i veřejných parametrů).**
4. Absenci validace TLS certifikátu pro navázané TCP spojení.

## 3. Ktoré tvrdenia nie sú správe?

1. Pri dnešných grafických kartách (napr. Nvidia RTX 4090) je úspešnosť slovníkových útokov voči heslám užívateľov 100% (do 24h)
2. Iteratívne hashovanie s použitím slabších hashovacích funkcii (MD5, SHA1) je imunné voči slovníkovým útokom
3. Hashovacia funkcia môže byť okrem iného (s použitím dostatočne silnej kryptografickej soli o dĺžke aspoň 192 bit) veľmi efektívna aj ako symetrická šifra
4. **Hashovacia funkcia `bcrypt` je násobne pomalšia ako funkcia `SHA-512`**

## 4. Která z těchto tvrzení jsou správná?

1. Zranitelnost aplikace lze opravit zavedením antivirového řešení na straně serveru.
2. Zranitelnost aplikace lze opravit zvýšením velikosti seedu na alespoň 128 bitů.
3. Seed kryptografického generátoru náhodných čísel je veřejný parametr generátoru.
4. Seed kryptografického generátoru náhodných čísel je tajný parametr generátoru.