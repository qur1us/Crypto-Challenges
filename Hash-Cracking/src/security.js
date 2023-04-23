const crypto = require('crypto');

class Security {
    static hashPassword(password) {
        // Used to append to user password so it's harder to crack
        const salt = "za1&P^tMvkvz#Xe%7B4j"
        
        let hash = password
        
        // Hash the password 1337 times so students cannot use john of hashcat
        for (let i = 0; i <= 1337; i++) {
            hash = crypto.createHash("md5").update(hash + salt).digest("hex");
        }
        
        return hash;
    }
}

module.exports = Security;
