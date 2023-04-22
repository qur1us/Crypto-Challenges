# Popis programu
Program realizující tuto úlohu vygeneruje dvě prvočísla, každé o velikosti 4096 bitů, z nich je následně vypočítán modulus, který aplikace odešle řešiteli. Ke komunikaci používá aplikace síťový port 1337.

```go
---8<---
p, _ := rand.Prime(rand.Reader, BITSIZE)
---8<---
q, _ := rand.Prime(rand.Reader, BITSIZE)
---8<---
n := big.NewInt(0)
n = n.Mul(p, q)
conn.Write([]byte("\nn: " + toHexInt(n)))
```

Alice a Bob si zvolí veřejné klíče, jako veřejné klíče byla zvolena dvě Fermatova prvočísla - 65537 a 257. Tato čísla byla vybrána, protože umožňují rychlé modulární mocnění.

Pro Alici a Boba je následně vytvořen i privátní klíč. Privátní klíče nejsou využity, jejich generování v programu však není nadbytečné. Pro řešitele se jedná o jasnou indicii, že se jedná o algoritmus RSA. 
```go
func rsa_keygen(p *big.Int, q *big.Int, e *big.Int) *big.Int {

	phi_n, d, pminus1, qminus1, bigOne := big.NewInt(0), big.NewInt(0), big.NewInt(0), big.NewInt(0), big.NewInt(1)

	//Calculate modulus (n) and Euler Phi of n (phi_n)
	pminus1, qminus1 = pminus1.Sub(p, bigOne), qminus1.Sub(q, bigOne)
	phi_n = phi_n.Mul(pminus1, qminus1)

	//Calculate private key
	d = d.ModInverse(e, phi_n)

	return d
}
```

Vlajka je poté zašifrována veřejným klíčem Alice i Boba, řešitel obdrží modulus, veřejné klíče Alice a Boba, šifrové texty Alice a Boba. Ukázkový výstup aplikace:
```
Generating primes... (this might take a while)

First prime found.
Second prime found.

Calculating modulus...
n: 0xd0---8<---e7

Generating keys...

Alice's Public Key: 0x10001
Bob's Public Key: 0x101

Alice's encrypted flag: 0x11---8<---09

Bob's encrypted flag: 0x6a---8<---16

Closing channel.
```

## Spuštění programu
Ke spuštění programu je potřeba mít nainstalovaný balíček `golang`.
Ten lze získat například příkazem:
```shell
$ sudo apt install golang -y
```

Poté stačí ve složce se `server.go` spustit následující příkaz:
```shell
$ go run .
```

# Popis zranitelnosti
Zranitelnost programu spočívá v tom, že Alice a Bob používají stejná prvočísla pro vygenerování klíčů a odesílají stejnou zprávu.
```go
Alice_priv := rsa_keygen(p, q, Alice_pub)
Bob_priv := rsa_keygen(p, q, Bob_pub)
---8<---
Alice_cipher := encrypt(new(big.Int).SetBytes([]byte(FLAG)), Alice_pub, n)
Bob_cipher := encrypt(new(big.Int).SetBytes([]byte(FLAG)), Bob_pub, n)
```

Použití stejných prvočísel ($p$ a $q$) má za následek společný modulus $n$ a díky tomu, že veřejné klíče Alice ($e_1$) a Boba ($e_2$) jsou čísla nesoudělná, je možné pomocí rozšířeného Euklidova algoritmu získat zprávu v otevřeném textu.

## Důkaz zranitelnosti

Mějme tajnou zprávu $M$, veřejné klíče $e_1$, $e_2$ a šifrové texty $c_1 = M^{e_1}$, $c_2 = M^{e_2}$.
Pokud $e_1$ a $e_2$ jsou nesoudělná, tedy gcd($e_1$, $e_2$) = 1.

Pak platí:
$$xe_1 + ye_2 = 1$$
Potom:
$$c_1^x \cdot c_2^y = (M^{e_1})^x \cdot (M^{e_2})^y = M^{e_1x} \cdot M^{e_2y}=M^{e_1x + e_2y} = M^1$$

# Řešení
K řešení úlohy lze využít [tento](solver.py) script.