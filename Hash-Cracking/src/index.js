const express        = require('express');
const app            = express();

const session        = require("express-session");
const cookieParser   = require("cookie-parser");
const routes         = require('./routes');
const Database       = require('./database');

// Create the database and fill it with users and their passwords
const db = new Database("webapp.db");

db.connect();
db.init();

// Add users
db.addUser("admin", "billabong");
db.addUser("jack", "gasdgasdasdgasdgasdfasgrsgh");
db.addUser("alan", "cora2nasgadfhadfgasdfblack2");
db.addUser("charlie", "danae0ahdfadfgasdf07");

// Parse the POST data as application/json or application/x-www-form-urlencoded
app.use(express.json());
app.use(express.urlencoded({extended: true}));

// Let Express parse the cookies
app.use(cookieParser());

// Host static CSS files 
app.use(express.static('public'));

// Session management
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
