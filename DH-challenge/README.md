# Popis programu
Program realizující tuto úlohu vygeneruje prvočíslo ($p$) o velikosti 2048 bitů, zvolí generátor ($g = 7$), tyto informace pošle řešiteli. Ke komunikaci používá aplikace síťový port 1337.
```python
p = getPrime(2048)
g = 7
---8<---
sendMessage(s, f"\ng = {g}, p = {p}")
```

Pozn. Všechny následující výpočty jsou modulo $p$.
Náhodně zvolí tajný parametr ($a$) a vypočítá veřejný parametr ($A = g^a$).
```python
a = random.randrange(2, p - 1)
A = pow(g, a, p)
```

Od řešitele obdrží veřejný parametr ($B$), pomocí níž vypočítá hodnotu tajného klíče $k = B^a$.
```python
B = recieveMessage(s, "\nEnter Your Public Key: ")
---8<---
shared_secret = pow(B, a, p)
```

Tajným klíčem $k$ pak zašifruje pomocí AES-256-GCM vlajku a odešle ji řešiteli.
```python
result = encrypt(FLAG, shared_secret)
sendMessage(s, f"\nHere is The Encrypted Flag: {result}")
```

## Spuštění programu
Ke spuštění aplikace je potřeba mít nainstalovaný `python3` a moduly používané aplikací.
Instalaci modulů je velmi doporučeno provést do virtuálního prostředí (`venv`). K tomu lze uvnitř této složky použít následující příkazy:
```shell
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

# Popis zranitelnosti
Zranitelnost programu spočívá v tom, že program neověřuje hodnotu $B$. Řešitel může odeslat takové $B$, aby hodnota $k$ byla taková, kterou bude schopen získat bez znalosti $A$ nebo $a$. 
Ze zdrojového kódu je patrné, že $k = B^a$, řešitel tedy hledá takové $B$, pro které bude $k$ dobře reprodukovatelné. Parametr $B$ lze zvolit $0$, nebo $1$, pak i hodnota $k$ bude $0$, nebo $1$.
Pokud $B = 0$, pak $k = B^a = 0^a = 0$.
Pokud $B = 1$, pak  $k = B^a = 1^a = 1$.

Pomocí získaného $k$ pak může dešifrovat obdrženou zprávu a získat tak vlajku.

# Nápovědy
1. Zaměřte se na to jakým způsobem aplikace vypočítá klíč $k$, kterým zašifruje text vlajky.
2. Zkuste odeslat takové $B$, aby dohodnutý šifrovací klíč $k$ byl předvídatelný.
3. Zkuste odeslat $B=1$.
4. Bude obsahovat text vlajky.

# Řešení
K řešení úlohy lze využít [tento](solver.py) script.