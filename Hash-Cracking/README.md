# Slovníkový útok na vlastnú implementáciu hashovania hesiel vo webovej aplikácii

## Úloha do kybernetickej arény

Úloha pozostáva z analýzy úniku databádzy webovej aplikácie, kde sa nachádzajú zahashované heslá užívateľov a analýzy zdrojového kódu backendu webovej aplikácie. Úlohou študenta bude použiť logiku zdrojového kódu webovej aplikácie, ktorá sa stará o hashovanie a ukladanie hesiel do databázy a použiť ju do vlastnej implementácie slovníkového útoku.

Zdrojový kód zodpovedný za hashovanie hesiel používa hash typu MD5, avšak heslá užívateľov sú solené fixnou hodnotou dostupnou len z backendu a heslo prejde hashovacou funkciou niekoľko krát. Hash je teda vo formáte MD5 ale na jeho cracknutie nestačí software ako john alebo hashcat (základná konfigurácia bez zásahu do zdrojového kódu), študent musí slovníkový útok implementovať vlastným spôsobom.

K úlohe je dostupná aj webová aplikácia obsahujúca správu o tom, že chod webové stránky je kvôli kybernetickému útoku pozastavený a poskytne študentovi prihlasovací formulár pre administrátora webového serveru.

Po cracknutí hesla administrátora sa bude môcť študent do webovej aplikácie prihlásiť a tá mu poskytne flag a úloha bude považovaná za splnenú.

### Nápovede

Úloha bude obsahovať celkom 4 nápovede, každá bude dostupná s penalizáciou 25% bodového zisku za túto úlohu:

1.  Necrackovať pomocou software ako hashcat či john. Preskúmať akým spôsobom funguje hashovanie hesiel v 
zdrojovom kóde. Je potrebné použiť a vhodným spôsobom upraviť funkciu starajúcu sa o hashovanie a ukladanie do databázy a prispôsobiť na slovníkový útok vo vlastnom skripte.
2.  Pseudo kód pre implementáciu slovníkového útoku

```csharp
open file:
	readhashes()

	for hash in hashes:
		open file:
			readwordlist()

			foreach password in wordlist:
				hashpassword()
				
				if original == hashed_password:
					cracked = True
```

3. Zdrojový kód slovníkového útoku

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

4.  Bude obsahovať text vlajky - `FLAG{EVERY_HACKER_MUST_KNOW_SOME_JS}`

## Tvorba webovej aplikácie

Webová aplikácia bola vyvíjaná v programovacom jazyky **Node.js** a bol použitý webový framework **Express.js**. 

### Ovládanie webového rozhrania

Aplikácia obsahuje celkovo 4 routy, z toho 3 používajúce metódu `GET` a jedna metódu `POST`:

`/`
- Táto routa vráti študentovi jednoduchú webovú stránku s informáciou o fiktívnom kybernetickom útoku na webový server a odkáže ho na prihlasovací formulár.

`/login`
- Obsahuje webovú stránku a funkcionalitu prihlasovacieho formulára. Pomocou tohto formulára sa webovej aplikácii pošle `POST` request s prihlasovacími údajmi na na `/auth/login` endpoint a backend webovej aplikácie overí prihlasovacie údaje s údajmi v databáze. Ak študent zadá správne údaje, bude presmerovaný do routy `/dashboard`.

`/dashboard`
- Po úspešnom prihlásení, prístup na túto routu poskytne študentovi flag vo formáte `FLAG{xxxxxxx}`.

### Ukladanie hesiel do databázy

Súbor `database.js` obsahuje všetky potrebné funkcie pre prácu s `sqlite3` databázou. Samotná databáza sa vytvorí a naplní užívateľmi a heslami pri každom behu webovej aplikácie.

```js
// Create the database and fill it with users and their passwords
const db = new Database("webapp.db");

db.connect();
db.init();

// Add users
db.addUser("admin", "billabong");
db.addUser("jack", "gasdgasdasdgasdgasdfasgrsgh");
db.addUser("alan", "cora2nasgadfhadfgasdfblack2");
db.addUser("charlie", "danae0ahdfadfgasdf07");
```

Webová aplikácia nie je priamo súčasťou challengu. Ide hlavne o súbor `security.js`, v ktorom sa nachádza funkcia `hashPassword`, ktorú obsahuje vlastnú implementáciu hashovania hesiel s použitím hashovacej funkcie MD5.

```js
static hashPassword(password) {
        const salt = "za1&P^tMvkvz#Xe%7B4j"
        
        let hash = password
    
        for (let i = 0; i <= 1337; i++) {
            hash = crypto.createHash("md5").update(hash + salt).digest("hex");
        }

		return hash;
    }
```

Funkcia používa `salt`, ktorý pridáva za originálne heslo zadané používateľom. Nový hash hashuje 1337 krát a vždy k novému hashu pridá `salt`. Tým sa zaistí necrackovateľnosť bežným software ako [john](https://github.com/openwall/john) či [hashcat](https://hashcat.net/hashcat/) (základná konfigurácia bez zásahu do zdrojového kódu).

### Logovanie

Webová aplikácia poskytuje aj jednoduché konzolové logovanie jednotlivých requestov:

```text
➜  src git:(main) ✗ node index.js
[+] App is running on port 3000.
.
.
GET / from ::ffff:192.168.220.1
GET /login from ::ffff:192.168.220.1
POST /auth/login from ::ffff:192.168.220.1
[-] Login failed => admin:wrongpassword
GET /login from ::ffff:192.168.220.1
POST /auth/login from ::ffff:192.168.220.1
[+] Login successful => admin:billabong
GET /dashboard from ::ffff:192.168.220.1
```

### Štruktúra

```bash
├── public
│   └── css
│       └── style.css
├── routes
│   └── index.js
├── views
│   ├── index.html
│   └── login.html
├── database.js
├── security.js
├── index.js
├── package.json
├── package-lock.json
└── webapp.db
```

## Inštalácia balíčkov a spustenie webovej aplikácie

Inštalácia:

```text
cd Hash-Cracking/src
npm install
```

Spustenie webovej aplikácie:

```text
cd Hash-Cracking/src
node index.js
```

Úspešné spustenie aplikácie by malo vyzerať nasledovne:

```text
➜  src git:(main) ✗ node index.js
[+] App is running on port 3000.

[+] User admin added successfully. Hash: 0d9e0aace6207569832f3d5df72d7589
[+] User alan added successfully. Hash: 1aa601e825516fc648491e4c98e3898f
[+] User charlie added successfully. Hash: 09c8f81a561ab3efb21379b80d701fd7
[+] User jack added successfully. Hash: 45e986230061621f0f7b95e3913910f3
```

## Riešenie

Študent nemôže použiť nástroje ako [john](https://github.com/openwall/john) či [hashcat](https://hashcat.net/hashcat/) (základná konfigurácia bez zásahu do zdrojového kódu), ale musí vytvoriť vlastné riešenie. Súbor s implementovaným hashovacím algoritmu bude študentom poskytnutý spolu s uniknutými hashmi z databázy a slovníkom, ktorý budú môcť použiť. Ukážkové riešenie je možné vidieť v python3 skripte [tu](./solution/kraken.py).

```text
➜  Hash-Cracking git:(main) ✗ python3 solution/kraken.py solution/leak.txt solution/wordlist.txt
Cracking 1aa601e825516fc648491e4c98e3898f
[-] Failed to crack.

Cracking 09c8f81a561ab3efb21379b80d701fd7
[-] Failed to crack.

Cracking 0d9e0aace6207569832f3d5df72d7589
[+] Hash cracked: billabong

Cracking 45e986230061621f0f7b95e3913910f
[-] Failed to crack.
```