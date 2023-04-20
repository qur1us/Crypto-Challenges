package main

import (
	"crypto/rand"
	"fmt"
	"math/big"
)

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
	flag := []byte("FLAG{n3vEr_3Ver_sH4r3_pR1m35_w1tH_y0Ur_fR13nd5}") //FLAG{WiTh_fR13nd5_5h4r3_m3m0r13s_d0n't_sH4r3_y0Ur_pR1m35!}

	//Generate safe primes for RSA
	p, _ := rand.Prime(rand.Reader, 4096)
	q, _ := rand.Prime(rand.Reader, 4096)

	fmt.Println("\nGenerating primes...")
	fmt.Println("p: ", p)
	fmt.Println("q: ", q)

	n := big.NewInt(0)
	n = n.Mul(p, q)

	fmt.Println("\nCalculating modulus...")
	fmt.Println("n: ", n)

	//Use Fermat primes as public keys
	Alice_pub, Bob_pub := big.NewInt(65537), big.NewInt(257)
	fmt.Println("\nGenerating keys...")

	Alice_priv := rsa_keygen(p, q, Alice_pub)
	Bob_priv := rsa_keygen(p, q, Bob_pub)

	//suppress compilation error
	_, _ = Alice_priv, Bob_priv

	fmt.Println("Alice Public Key: ", Alice_pub)
	fmt.Println("Bob Public Key: ", Bob_pub)

	Alice_cipher := encrypt(new(big.Int).SetBytes(flag), Alice_pub, n)
	Bob_cipher := encrypt(new(big.Int).SetBytes(flag), Bob_pub, n)

	fmt.Println("\nAlice's encrypted flag: ", Alice_cipher)
	fmt.Println("\nBob's encrypted flag: ", Bob_cipher)

	///fmt.Println("\nPlaintext: ", new(big.Int).SetBytes(flag))
}
