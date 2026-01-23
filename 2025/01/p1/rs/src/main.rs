use std::fs::File;
use std::io::{BufRead, BufReader};
use std::path::PathBuf;

fn get_data(file_name: &str) -> Vec<i16> {
    let path: PathBuf = ["..", "..", "data", file_name].iter().collect();
    let display = path.display();
    let file: File = match File::open(&path) {
        Err(e) => panic!("could not open {}: {}", display, e),
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
            Ok(v) => v,
        };

        ret.push(value * direction);
    }

    return ret;
}

fn main() {
    // let file_name = "example.txt";
    let file_name = "input.txt";

    let mut pos: i16 = 50;
    let mut counter: i16 = 0;
    for val in get_data(file_name) {
        pos += val % 100;

        if pos >= 99 {
            pos -= 100;
        } else if pos <= -100 {
            pos += 100;
        }

        if pos == 0 {
            counter += 1;
        }
    }

    println!("counter={:?}", counter);
}
