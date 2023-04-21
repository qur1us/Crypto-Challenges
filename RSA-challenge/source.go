package main

import (
	"crypto/rand"
	"fmt"
	"math/big"
)

func toHexInt(n *big.Int) string {
	return fmt.Sprintf("0x%x", n) // or %x or upper case
}

func rsa_keygen(p *big.Int, q *big.Int, e *big.Int) *big.Int {

	phi_n, d, pminus1, qminus1, bigOne := big.NewInt(0), big.NewInt(0), big.NewInt(0), big.NewInt(0), big.NewInt(1)

	//Calculate modulus (n) and Euler Phi of n (phi_n)
	pminus1, qminus1 = pminus1.Sub(p, bigOne), qminus1.Sub(q, bigOne)
	phi_n = phi_n.Mul(pminus1, qminus1)

	//Calculate private key
	d = d.ModInverse(e, phi_n)

	return d
}

func encrypt(message *big.Int, key *big.Int, n *big.Int) *big.Int {
	cipher := big.NewInt(0)
	cipher = cipher.Exp(message, key, n)
	return cipher
}

func main() {
	flag := []byte("FLAG{---REDACTED---}")

	//Generate safe primes for RSA
	fmt.Println("\nGenerating primes...")
	p, _ := rand.Prime(rand.Reader, 4096)
	fmt.Println("\nFirst prime found.")
	q, _ := rand.Prime(rand.Reader, 4096)
	fmt.Println("\nSecond prime found.")

	//fmt.Println("p: ", p)
	//fmt.Println("q: ", q)

	fmt.Println("\nCalculating modulus...")
	n := big.NewInt(0)
	n = n.Mul(p, q)
	fmt.Println("n: ", toHexInt(n))

	//Use Fermat primes as public keys -> faster modular exponentiation
	Alice_pub, Bob_pub := big.NewInt(65537), big.NewInt(257)
	fmt.Println("\nGenerating keys...")

	Alice_priv := rsa_keygen(p, q, Alice_pub)
	Bob_priv := rsa_keygen(p, q, Bob_pub)

	//suppress compilation error
	_, _ = Alice_priv, Bob_priv

	fmt.Println("Alice Public Key: ", toHexInt(Alice_pub))
	fmt.Println("Bob Public Key: ", toHexInt(Bob_pub))

	Alice_cipher := encrypt(new(big.Int).SetBytes(flag), Alice_pub, n)
	Bob_cipher := encrypt(new(big.Int).SetBytes(flag), Bob_pub, n)

	fmt.Println("\nAlice's encrypted flag: ", toHexInt(Alice_cipher))
	fmt.Println("\nBob's encrypted flag: ", toHexInt(Bob_cipher))
}
