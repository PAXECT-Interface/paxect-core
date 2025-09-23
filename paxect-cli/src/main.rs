use std::env;
use std::io::{self, Read, Write};

// importeer de core lib-naam
use paxect_core_rs as core;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 || (args[1] != "encode" && args[1] != "decode") {
        eprintln!("Usage: paxect <encode|decode>");
        std::process::exit(1);
    }

    // lees alle stdin
    let mut input = Vec::new();
    if let Err(e) = io::stdin().read_to_end(&mut input) {
        eprintln!("Failed to read stdin: {e}");
        std::process::exit(1);
    }

    // core aanroepen
    let output = if args[1] == "encode" {
        core::encode(&input)
    } else {
        match core::decode(&input) {
            Ok(v) => v,
            Err(e) => {
                eprintln!("Decode error: {e}");
                std::process::exit(2);
            }
        }
    };

    // schrijf naar stdout
    if let Err(e) = io::stdout().write_all(&output) {
        eprintln!("Failed to write stdout: {e}");
        std::process::exit(1);
    }
}
