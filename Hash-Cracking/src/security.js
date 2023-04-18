const crypto = require('crypto');

class Security {
    static hashPassword(password) {
        const salt = "za1&P^tMvkvz#Xe%7B4j"
        
        let hash = password
    
        for (let i = 0; i <= 1337; i++) {
            hash = crypto.createHash("md5").update(hash + salt).digest("hex");
        }
        
        console.log(hash);

        return hash;
    }
}

module.exports = Security;
