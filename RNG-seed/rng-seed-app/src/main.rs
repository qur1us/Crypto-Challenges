use chrono::NaiveDateTime;
use rand_chacha::rand_core::{RngCore, SeedableRng};
use rand_chacha::ChaCha20Rng;
use regex::Regex;
use std::collections::{HashMap, HashSet};
use std::io::{Read, Write};
use std::net::{SocketAddr, TcpListener, TcpStream};
use std::sync::{Arc, Mutex};
use std::time::{Duration, SystemTime, UNIX_EPOCH};
use std::{fs, thread};

/* TODO
 * unwraps
 */

const TITLE: &[u8; 31] = b"Temporary password manager v1.3";
const MENU: &[u8; 117] = b"

1) Add password
2) Export passwords
3) Download exported passwords
4) Exit
9) [DEV] Print application log

Option: ";

#[derive(Debug)]
enum LogLevel {
    DEBUG,
    INFO,
    ERROR,
}

/// Groups all relevant data important for handling client sessions
struct ClientSession {
    socket: TcpStream,
    addr: SocketAddr,
    passwords: HashMap<String, HashSet<String>>,
    logs: Arc<Mutex<Vec<String>>>,
}

impl ClientSession {
    /// Stores a client's password for any given domain
    ///
    /// Allows multiple passwords for 1 domain
    fn add_password(&mut self) {
        self.send(b"[*] Domain: ");
        let domain = self.recv();

        self.send(b"[*] Password: ");
        let password = self.recv();

        // Check if the domain already exists
        match self.passwords.get_mut(&domain) {
            Some(pass_set) => {
                // If it does, just add another password
                pass_set.insert(password);
            }
            None => {
                // If it does not, create a new hashset for it
                self.passwords.insert(domain, HashSet::from([password]));
            }
        }

        self.send(b"[+] Password stored securely");

        log(
            LogLevel::INFO,
            self,
            get_timestamp(),
            String::from("Password stored securely"),
        );
    }

    /// Securely exports client's passwords
    fn export_passwords(&mut self) {
        let filename = generate_secure_filename(self);

        // Fake delay to make the filename generation feel even more secure
        self.send(b"[*] Generating a secret filename (this may take several seconds)");
        thread::sleep(Duration::from_secs_f32(2.345));

        // Write the passwords to a file
        let mut file = fs::File::create(&filename).unwrap();
        write!(file, "{:?}", self.passwords).unwrap();

        self.send(format!("[+] Passwords exported as '{}'", filename).as_bytes());

        log(
            LogLevel::INFO,
            self,
            get_timestamp(),
            format!("Passwords exported"),
        );
    }

    /// Downloads a file containing client's exported passwords, specified by a TXT filename
    fn download_exported_passwords(&mut self) {
        self.send(b"[*] Filename: ");
        let filename = self.recv();

        // Filter invalid filenames
        let mut ok = false;
        let re = Regex::new(r"^[a-zA-Z0-9]*\.txt$").unwrap();

        if !re.is_match(&filename) {
            self.send(b"[!] Only txt files are supported\n[!] Example: a01b23c45d67e89f.txt");
        } else {
            match fs::read_to_string(&filename) {
                Ok(contents) => {
                    self.send(contents.as_bytes());
                    ok = true;
                }
                Err(_) => {
                    self.send(b"[!] The requested file does not exist");
                }
            }
        }

        if ok {
            log(
                LogLevel::INFO,
                self,
                get_timestamp(),
                format!("Downloaded exported passwords"),
            );
        } else {
            log(
                LogLevel::ERROR,
                self,
                get_timestamp(),
                format!("Failed attempt to download exported passwords"),
            );
        }
    }

    /// Downloads the application log
    ///
    /// Intended primarily for developers
    fn download_app_log(&mut self) {
        let mut log_messages = String::new();

        // Convert the vector of strings into 1 multiline string
        for str in self.logs.lock().unwrap().iter() {
            log_messages.push_str(str);
            log_messages.push('\n');
        }

        // Remove the last newline
        log_messages.pop();

        self.send(log_messages.as_bytes());
        log(
            LogLevel::DEBUG,
            self,
            get_timestamp(),
            String::from("Downloaded application logs"),
        );
    }

    /// Wrapper for `TcpStream.write(msg)` that handles errors
    fn send(&mut self, msg: &[u8]) {
        match self.socket.write(msg) {
            Ok(_) => (),
            Err(e) => {
                log(
                    LogLevel::ERROR,
                    self,
                    get_timestamp(),
                    String::from("Connection error"),
                );
                panic!("{e}");
            }
        };
    }

    /// Wrapper for `TcpStream.read(&mut data)` that
    /// handles errors and returns a cleaned String
    fn recv(&mut self) -> String {
        let mut data = [0; 256];

        match self.socket.read(&mut data) {
            Ok(_) => (),
            Err(e) => {
                log(
                    LogLevel::ERROR,
                    self,
                    get_timestamp(),
                    String::from("Connection error"),
                );
                panic!("{e}");
            }
        }

        // Convert the received bytes to String and remove newline and null-bytes
        let data = std::str::from_utf8(&data)
            .unwrap()
            .trim_end_matches([char::from(0), char::from(10)]);

        return String::from(data);
    }
}

/// Handles a client session and all their operations
///
/// Intended for multithreaded execution for all individual clients
fn handle_client(socket: TcpStream, addr: SocketAddr, logs: Arc<Mutex<Vec<String>>>) {
    let mut client = ClientSession {
        addr: addr,
        logs: logs,
        socket: socket,
        passwords: HashMap::new(),
    };

    log(
        LogLevel::INFO,
        &client,
        get_timestamp(),
        String::from("Connected"),
    );

    client.send(TITLE);

    // Control menu
    loop {
        client.send(MENU);
        let request = client.recv();
        client.send(b"\n");

        match &request[..] {
            "1" => client.add_password(),
            "2" => client.export_passwords(),
            "3" => client.download_exported_passwords(),
            "9" => client.download_app_log(),
            "4" => {
                client.send(b"[+] Terminating connection");
                break;
            }
            _ => {
                client.send(b"[!] Unknown option!");
            }
        }
    }

    log(
        LogLevel::INFO,
        &client,
        get_timestamp(),
        String::from("Disconnected"),
    );
}

/// Create a random TXT filename generated by a secure cryptographic RNG (`ChaCha20Rng`)
fn generate_secure_filename(client: &ClientSession) -> String {
    let timestamp = get_timestamp();

    // Reuse the log timestamp to save resources
    let random = ChaCha20Rng::seed_from_u64(timestamp).next_u64();

    let filename = format!("{random:x}.txt");

    log(
        LogLevel::DEBUG,
        client,
        timestamp,
        String::from("Random filename generated"),
    );

    return filename;
}

/// Add an application log entry
///
/// All client threads contribute to the same application log
fn log(level: LogLevel, client: &ClientSession, timestamp: u64, msg: String) {
    // UTC time
    let time = NaiveDateTime::from_timestamp_opt(timestamp as i64, 0).unwrap();

    let logmessage = format!(
        "[{} (UTC)] [{:?}] ({}) {msg}",
        time.format("%F %T"),
        level,
        client.addr
    );

    // Log everything to server console
    println!("{logmessage}");

    let mut logs = client.logs.lock().unwrap();
    logs.push(logmessage);
}

/// Current UTC time in UNIX timestamp
fn get_timestamp() -> u64 {
    return SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap()
        .as_secs();
}

fn main() {
    let listener;

    loop {
        match TcpListener::bind("0.0.0.0:31337") {
            Ok(val) => {
                listener = val;
                break;
            }
            Err(_) => (),
        }
    }

    // Logs shared among all client threads
    let logs = Arc::new(Mutex::new(Vec::<String>::new()));

    loop {
        match listener.accept() {
            Ok((socket, addr)) => {
                let logs = Arc::clone(&logs);

                thread::spawn(move || {
                    handle_client(socket, addr, logs);
                });
            }
            Err(_) => (),
        }
    }
}
