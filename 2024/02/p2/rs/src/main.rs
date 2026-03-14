use std::fs::File;
use std::io::{BufRead, BufReader};
use std::path::PathBuf;

fn get_path() -> PathBuf {
    let args: Vec<String> = std::env::args().collect();
    let name: &str;
    if args.len() <= 1 || args[1].len() == 0 {
        name = "example.txt"
    } else {
        name = args[1].as_str();
    }
    return PathBuf::from_iter(["..", "..", "..", "data", name]);
}

fn get_data(path: &PathBuf) -> Result<Vec<Vec<i16>>, Box<dyn std::error::Error>> {
    println!("opening {:?}", path.canonicalize());

    let file = File::open(&path)?;
    let reader = BufReader::new(file);
    let mut ret: Vec<Vec<i16>> = vec![];

    for line in reader.lines() {
        let s = line?.split_whitespace()
                     .map(|s| s.parse::<i16>().expect("could not parse value"))
                     .collect::<Vec<i16>>();

        if s.len() > 0 {
            ret.push(s);
        }
    }

    return Ok(ret);
}

fn check_levels(lvls: &[i16]) -> bool {
    if lvls.len() < 2 { return true; }
    let mut diff: i16 = lvls[1] - lvls[0];
    let direction: i8 = match diff {
        1..=3 => 1,
        -3..=-1 => -1,
        _ => return false,
    };
    let mut i = 2usize;
    while i < lvls.len() {
        diff = lvls[i] - lvls[i-1];
        match diff {
            0 => return false,
            ..=-4 | 1.. if direction < 1 => return false,
            ..0 | 4.. if direction > 0 => return false,
            _ => i += 1,
        }
    }
    return true;
}

fn main() {
    let path = get_path();
    let data = get_data(&path).expect("could not get data due to error");
    let mut counter = 0i16;

    'main: for d in data {
        if d.len() <= 2 { continue; }
        if check_levels(&d[..]) {
            counter += 1;
            continue;
        }

        for i in 0..d.len() {
            let s = [&d[..i], &d[i+1..]].concat();
            if check_levels(&s) {
                counter += 1;
                continue 'main;
            }
        }
    }

    println!("counter={:?}", counter);
}
