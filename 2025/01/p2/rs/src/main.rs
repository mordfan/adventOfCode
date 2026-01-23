use std::fs::File;
use std::io::{BufRead, BufReader};
use std::path::PathBuf;

fn get_file_path() -> PathBuf {
    let args: Vec<String> = std::env::args().collect();
    let file_name: &str;
    if args.len() <= 1 || args[1].len() == 0 {
        file_name = "example.txt"
    } else {
        file_name = args[1].as_str();
    }
    let path: PathBuf = ["..", "..", "data", file_name].iter().collect();
    return path;
}

fn get_data(file_path: PathBuf) -> Vec<i16> {
    println!("opening {:?}", file_path.display());

    let file: File = match File::open(&file_path) {
        Err(e) => panic!("could not open {}: {}", file_path.display(), e),
        Ok(file) => file,
    };

    let mut ret: Vec<i16> = Vec::new();
    let reader = BufReader::new(file);
    let mut line_no = 0;
    for line in reader.lines() {
        line_no += 1;

        let content = match line {
            Err(_) => panic!("could not read line no={}", line_no),
            Ok(content) => content,
        };

        let direction = match content.get(..1) {
            Some("L") => -1,
            Some("R") => 1,
            _ => panic!("could not parse direction in line no={}", line_no),
        };

        let value = match content[1..].parse::<i16>() {
            Err(_) => panic!("could not parse line no={}", line_no),
            Ok(value) => value,
        };

        ret.push(value * direction);
    }

    return ret;
}

fn main() {
    let path = get_file_path();

    let mut pos: i16 = 50;
    let mut counter: i16 = 0;

    for clicks in get_data(path) {
        let prev = pos;
        let mut change: i16 = (clicks / 100).abs();
        pos += clicks % 100;

        if pos > 99 {
            pos -= 100;
            change += 1;
        } else if pos < -99 {
            pos += 100;
            change += 1;
        } else if prev < 0 && pos > 0 {
            change += 1;
        } else if prev > 0 && pos < 0 {
            change += 1;
        } else if pos == 0 {
            change += 1;
        }

        counter += change;

        // println!("{prev:>5}{clicks:>5}={pos:>4}, {counter:>4}, {change:+}")
    }

    println!("counter={:?}", counter);
}
