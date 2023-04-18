const express        = require('express');
const app            = express();

const session        = require("express-session");
const cookieParser   = require("cookie-parser");

const routes         = require('./routes');
const Database       = require('./database');

const db = new Database("webapp.db");

// Init
db.connect();
db.init();
db.addUser("admin", "billabong");
db.addUser("jack", "gasdgasdasdgasdgasdfasgrsgh");
db.addUser("alan", "cora2nasgadfhadfgasdfblack2");
db.addUser("charlie", "danae0ahdfadfgasdf07");

// Parse the POST data as application/json or application/x-www-form-urlencoded
app.use(express.json());
app.use(express.urlencoded({extended: true}));
app.use(cookieParser());
app.use(express.static('public'));
app.use(session({
    secret: '7ceaf94a886734fa67508f280d0f1eaa',
    resave: false,
    saveUninitialized: false
}));

// Imports routes from ./routes/
app.use(routes);

// Create a listener on port 3000
app.listen(3000, function() {
    console.log("[+] App is running on port 3000.\n");
});
