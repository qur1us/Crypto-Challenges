const sqlite3    = require('sqlite3');
const Security   = require('./security');

class Database {

    constructor(db_file) {
        this.db_file = db_file;
        this.db = undefined;
        this.loggedIn = false;
    }

    connect() {
        // Connecnt to the local sqlite3 file
        this.db = new sqlite3.Database(this.db_file)
    }

    init() {
        // Create tables for users and thier passwords
        let query = `
            DROP TABLE IF EXISTS users;

            CREATE TABLE IF NOT EXISTS users (
                id         INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                username   VARCHAR(255) NOT NULL UNIQUE,
                password   VARCHAR(255) NOT NULL
            );`;

        this.db.exec(query);
    }

    addUser(username, password) {
        // Hash the password using the special MD5 hashing implementation
        const hash = Security.hashPassword(password);
        
        // Using prepared statement insert user and their password hash into the database
        let stmt = this.db.prepare("INSERT INTO users (username, password) VALUES (?,?)");

        stmt.run(username, hash, (err) => {
            if (err) {
                console.log("Query failed!");
            } else {
                console.log(`[+] User ${username} added successfully. Hash: ${hash}`)
            }
        });
    }
}

module.exports = Database;
