package main

import (
	"crypto/rand"
	"fmt"
	"log"
	"math/big"
	"net"
	"os"
)

const (
	HOST    = "localhost"
	PORT    = "1337"
	TYPE    = "tcp"
	FLAG    = "FLAG{SuP3r_S3cRe7_fL4g_f0R_T3s71nG}"
	BITSIZE = 4096
)

func toHexInt(n *big.Int) string {
	return fmt.Sprintf("0x%x", n)
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

func handleIncomingRequest(conn net.Conn) {
	//Generate safe primes for RSA
	conn.Write([]byte("\nGenerating primes... (this might take a while)"))
	p, _ := rand.Prime(rand.Reader, BITSIZE)
	conn.Write([]byte("\nFirst prime found."))
	q, _ := rand.Prime(rand.Reader, BITSIZE)
	conn.Write([]byte("Second prime found."))

	conn.Write([]byte("\nCalculating modulus..."))
	n := big.NewInt(0)
	n = n.Mul(p, q)
	conn.Write([]byte("\nn: " + toHexInt(n)))

	//Use Fermat primes as public keys -> faster modular exponentiation
	Alice_pub, Bob_pub := big.NewInt(65537), big.NewInt(257)
	conn.Write([]byte("\n\nGenerating keys..."))

	Alice_priv := rsa_keygen(p, q, Alice_pub)
	Bob_priv := rsa_keygen(p, q, Bob_pub)

	fmt.Println("[*] Key generation completed.")

	//suppress compilation error (unused variable)
	_, _ = Alice_priv, Bob_priv

	conn.Write([]byte("\nAlice's Public Key: " + toHexInt(Alice_pub)))
	conn.Write([]byte("\nBob's Public Key: " + toHexInt(Bob_pub)))

	Alice_cipher := encrypt(new(big.Int).SetBytes([]byte(FLAG)), Alice_pub, n)
	Bob_cipher := encrypt(new(big.Int).SetBytes([]byte(FLAG)), Bob_pub, n)

	conn.Write([]byte("\n\nAlice's encrypted flag: " + toHexInt(Alice_cipher)))
	conn.Write([]byte("\n\nBob's encrypted flag: " + toHexInt(Bob_cipher)))
	fmt.Println("[*] Flags sent.")
	conn.Write([]byte("\nClosing channel."))

	// close conn
	conn.Close()
	fmt.Println("[*] Channel closed.")

}

func main() {

	listen, err := net.Listen(TYPE, HOST+":"+PORT)
	fmt.Println("[*] Server running.")
	if err != nil {
		log.Fatal(err)
		os.Exit(1)
	}
	// close listener
	defer listen.Close()
	for {
		conn, err := listen.Accept()
		if err != nil {
			log.Fatal(err)
			os.Exit(1)
		}
		go handleIncomingRequest(conn)
	}
}
