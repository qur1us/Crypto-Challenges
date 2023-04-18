const path         = require('path');
const serialize    = require('node-serialize');
const express      = require('express');
const router       = express.Router();

const Database     = require('../database');
const Security     = require('../security');

const needsAuth = (req, res, next) => {
    if (req.session.isAuth) {
        next();
    } else {
        res.redirect("./login");
    }
}

const logRequest = (req, res, next) => {
    console.log(`${req.method} ${req.path} from ${req.ip}`);
    next();
}

router.get("/", logRequest, (req, res) => {
    req.session.isAuth = true;
    return res.sendFile(path.resolve("views/index.html"));
});

router.get("/login", logRequest, (req, res) => {
    req.session.isAuth = true;
    return res.sendFile(path.resolve("views/login.html"));
});

router.post("/auth/login", logRequest, (req, res) => {

    const { username, password } = req.body;

    const db = new Database("webapp.db");
    db.connect();
 
    const hash = Security.hashPassword(password);

    let stmt = db.db.prepare("SELECT username FROM users WHERE username = ? AND password = ?");

    stmt.get(username, hash, (err, row) => {

        if (err) {
            console.log("Query failed!");
            return res.redirect('/login');
        }

        if (row !== undefined) {
            console.log("[+] Login successful.");

            const cookie = JSON.stringify({
                "username": username,
                "loggedIn": Date.now()
            });
        
            const encodedCookie = Buffer(cookie).toString('base64');
        
            res.cookie("VUT", encodedCookie, { 
                maxAge: 6000 * 60 * 24,
                httpOnly: true,
                Path: "/dashboard"
            });

            return res.redirect('/dashboard');
        } else {
            console.log("[-] Login failed.");
            return res.redirect('/login');
        }
    });
});

router.get("/dashboard", needsAuth, logRequest, (req, res) => {
    const cookie = req.cookies.VUT;
    
    if (cookie) {
        const cookieData = Buffer(cookie, 'base64').toString();
        
        // Unsafe. Change to JSON.parse()
        let username = serialize.unserialize(cookieData).username;

        return res.send(`<script>alert("User ${username} logged in!")</script><h1>FLAG{EVERY_HACKER_MUST_KNOW_SOME_JS}</h1>`);
    } else {
        return res.sendStatus(403);
    } 
});

module.exports = router
