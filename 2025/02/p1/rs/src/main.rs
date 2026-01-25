use std::fs::File;
use std::io::{BufReader, BufRead};
use std::path::PathBuf;

fn open_file() -> File {
    let args: Vec<String> = std::env::args().collect();
    let file_name: &str;
    if args.len() <= 1 || args[1].len() == 0 {
        file_name = "example.txt"
    } else {
        file_name = args[1].as_str();
    }
    let path: PathBuf = ["..", "..", "..", "data", file_name].iter().collect();

    println!("opening {:?}", path.canonicalize());
    let file: File = match File::open(&path) {
        Err(e) => panic!("could not open {:?}: {}", path.canonicalize(), e),
        Ok(file) => file,
    };

    return file;
}

fn get_data() -> Vec<(u64, u64)> {
    let file = open_file();
    let reader = BufReader::new(file);
    let mut line_no = 0;

    let mut ret: Vec<(u64, u64)> = Vec::new();
    for line in reader.lines() {
        line_no += 1;

        let content: String = match line {
            Err(_) => panic!("could not read line no={}", line_no),
            Ok(content) => content,
        };

        let s: usize = match content.find("-") {
            None => panic!("no separator found in line no {}", line_no),
            Some(pos) =>  match pos {
                0 => panic!("invalid separator placement in line no {}", line_no),
                pos => pos,
            },
        };

        let start: u64 = match content[..s].parse::<u64>() {
            Err(_) => panic!("could not parse line no {}", line_no),
            Ok(value) => value,
        };

        let stop: u64 = match content[s+1..].parse::<u64>() {
            Err(_) => panic!("could not parse line no {}", line_no),
            Ok(value) => value,
        };

        ret.push((start, stop));
    }

    return ret;
}

fn main() {
    let mut score: u64 = 0;
    for (start, stop) in get_data() {
        for n in start..=stop {
            let s: String = n.to_string();
            if s.len() % 2 != 0 { continue; }
            let m = s.len() / 2;
            if s[..m] != s[m..] { continue; }
            score += n as u64;
        }
    }

    println!("score={}", score);
}
