const sqlite3 = require('sqlite3');
const Security = require('./security');

class Database {

    constructor(db_file) {
        this.db_file = db_file;
        this.db = undefined;
        this.loggedIn = false;
    }

    connect() {
        this.db = new sqlite3.Database(this.db_file)
    }

    init() {
        let query = `
            DROP TABLE IF EXISTS users;

            CREATE TABLE IF NOT EXISTS users (
                id         INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                username   VARCHAR(255) NOT NULL UNIQUE,
                password   VARCHAR(255) NOT NULL
            );`;

        this.db.exec(query);

        query = `
            DROP TABLE IF EXISTS sessions;

            CREATE TABLE IF NOT EXISTS sessions (
                id         INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                username   VARCHAR(255) NOT NULL UNIQUE,
                cookie     VARCHAR(255) NOT NULL
            );`;

        this.db.exec(query);
    }

    addUser(username, password) {
        const hash = Security.hashPassword(password);
        
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
