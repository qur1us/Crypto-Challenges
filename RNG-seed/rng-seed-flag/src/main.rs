use rand::{thread_rng, Rng};
use std::time::Duration;
use std::{io::Write, net::TcpStream};

fn sleep_rng() {
    let mut val;

    loop {
        val = thread_rng().gen::<u16>();
        if val > 2500 && val < 6000 {
            break;
        }
    }

    std::thread::sleep(Duration::from_millis(val as u64));
}

fn main() {
    let mut stream = TcpStream::connect("127.0.0.1:31337").unwrap();

    let requests = [
        "1",                                     // Add password
        "_FLAG_",                                // domain
        "FLAG{kE3p_s3eD_sEcr37_K3eP_SE3d_5aF3}", // password
        "2",                                     // Export passwords
        "4",                                     // Exit
    ];

    for request in requests {
        stream.write(request.as_bytes()).unwrap();

        // Random delay to simulate user input. The times are then visible in the log
        sleep_rng();
    }
}
