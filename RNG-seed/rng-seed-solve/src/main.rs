use chrono::NaiveDateTime;
use rand_chacha::{
    rand_core::{RngCore, SeedableRng},
    ChaCha20Rng,
};
use regex::Regex;
use std::thread::sleep;
use std::time::Duration;
use std::{
    io::{Read, Write},
    net::TcpStream,
};

fn main() {
    let mut stream = TcpStream::connect("127.0.0.1:31337").unwrap();
    let mut buffer = [0; 1024];

    // Read title and menu
    sleep(Duration::from_secs(1));
    stream.read(&mut buffer).unwrap();

    // Read logs
    stream.write(b"9").unwrap();
    sleep(Duration::from_secs(1));

    buffer.fill(0);
    stream.read(&mut buffer).unwrap();

    // Find RNG timestamp line
    let data = std::str::from_utf8(&buffer).unwrap();
    let rng_event = data
        .lines()
        .find(|x| x.contains("Random filename generated"))
        .unwrap();

    // Extract the time and date
    let re = Regex::new(r"^\[(.*?) (.*?) .*$").unwrap();
    let captures = re.captures(rng_event).unwrap();
    let date = &captures[1];
    let time = &captures[2];

    // ---------- EXPECTED STUDENT SOLUTION ----------

    // Reconstruct timestamp
    let datetime =
        NaiveDateTime::parse_from_str(&format!("{date} {time}")[..], "%Y-%m-%d %H:%M:%S").unwrap();

    let timestamp = datetime.timestamp() as u64;

    // Recreate filename
    let random = ChaCha20Rng::seed_from_u64(timestamp).next_u64();
    let filename = format!("{random:x}.txt");

    // ---------- EXPECTED STUDENT SOLUTION ----------

    // Get flag
    stream.write(b"3").unwrap();
    stream.write(filename.as_bytes()).unwrap();

    sleep(Duration::from_secs(1));
    buffer.fill(0);
    stream.read(&mut buffer).unwrap();

    // Clean disconnect
    stream.write(b"4").unwrap();
    sleep(Duration::from_secs(1));

    // Find FLAG line
    let data = std::str::from_utf8(&buffer).unwrap();
    let flag_line = data.lines().find(|x| x.contains("_FLAG_")).unwrap();

    // Extract the flag
    let re = Regex::new(r"^.*?(FLAG\{.*?\}).*?$").unwrap();
    let captures = re.captures(flag_line).unwrap();
    let flag = &captures[1];

    println!("{flag}");
}
