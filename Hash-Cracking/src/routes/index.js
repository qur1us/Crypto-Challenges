const path         = require('path');
const serialize    = require('node-serialize');
const express      = require('express');
const Database     = require('../database');
const Security     = require('../security');

const logRequest = (req, res, next) => {
    // Logs web application events to console
    console.log(`${req.method} ${req.path} from ${req.ip}`);
    next();
}

const router = express.Router();

router.get("/", logRequest, (req, res) => {
    return res.sendFile(path.resolve("views/index.html"));
});

router.get("/login", logRequest, (req, res) => {
    return res.sendFile(path.resolve("views/login.html"));
});

router.post("/auth/login", logRequest, (req, res) => {
    // Method parses the POST request and checks whether the entered data 
    // do have a match in the database, thus authenticating the user.

    // Parse the request
    const { username, password } = req.body;

    // Hash the password using the special MD5 hashing implementation
    const hash = Security.hashPassword(password);

    // Connect to the database
    const db = new Database("webapp.db");
    db.connect();
 
    // Using prepared statement, check the user-entered data with database entries
    let stmt = db.db.prepare("SELECT username FROM users WHERE username = ? AND password = ?");

    stmt.get(username, hash, (err, row) => {

        // Redirect to /login if the user-entered credentials are wrong
        if (err) {
            console.log("Query failed!");
            return res.redirect('/login');
        }

        // If login was succcessful, create custom cookie for the user 
        // session authentication and redirect to /dashboard to show 
        // the flag.
        if (row !== undefined) {
            console.log(`[+] Login successful => ${username}:${password}`);

            const cookie = JSON.stringify({
                "username": username,
                "loggedIn": Date.now()
            });
        
            const encodedCookie = Buffer.from(cookie).toString('base64');
        
            // Set the cookie
            res.cookie("secure_biscuit", encodedCookie, { 
                maxAge: 6000 * 60 * 24,
                httpOnly: true,
                Path: "/dashboard"
            });

            return res.redirect('/dashboard');
        } else {
            console.log(`[-] Login failed => ${username}:${password}`);
            return res.redirect('/login');
        }
    });
});

router.get("/dashboard", logRequest, (req, res) => {
    const cookie = req.cookies.secure_biscuit;
    
    // If the user has the "secure_biscuit" cookie, reveal the flag
    if (cookie) {
        const cookieData = Buffer.from(cookie, 'base64').toString();
        
        // Unsafe!
        //
        // Bonus task for the best of the best. The most successfull students
        // should be able to obtain Remote Code Execution capabilities and gain access
        // to the server this web application is hosted on.
        let username = serialize.unserialize(cookieData).username;

        return res.send(`<script>alert("User ${username} logged in!")</script><h1>FLAG{EVERY_HACKER_MUST_KNOW_SOME_JS}</h1>`);
    } else {
        return res.sendStatus(403);
    } 
});

module.exports = router
