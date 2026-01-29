use std::fs::File;
use std::io::{BufReader, BufRead};
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

fn get_data(path: &PathBuf) -> Result<Vec<Vec<u8>>, Box<dyn std::error::Error>> {
    println!("opening {:?}", path.canonicalize());

    let file = File::open(&path)?;
    let reader = BufReader::new(file);
    let mut line_no = 0;

    let mut ret = Vec::<Vec<u8>>::new();
    for line in reader.lines() {
        line_no += 1;
        let batteries: Vec<u8> = line.unwrap_or_else(|e| panic!("unable to read line {} => {}", line_no, e))
                                     .chars()
                                     .map(|c| c.to_string()
                                               .parse::<u8>()
                                               .unwrap_or_else(|e| panic!("could not parse value {} at line {} => {}", c, line_no, e)))
                                     .collect();
        ret.push(batteries);
    }

    return Ok(ret);
}

fn find_largest_joltage(batteries: &Vec<u8>) -> u8 {
    let mut ret = 0u8;
    let mut i = 0usize;

    //first battery
    if batteries[i] < 9 {
        for b in 1..(batteries.len() - 1) {
            if batteries[b] == 9 {
                i = b;
                break;
            } else if batteries[b] > batteries[i] {
                i = b
            }
        }
    }
    ret += batteries[i] * 10;

    //second battery
    i += 1;
    for b in i..batteries.len() {
        if batteries[b] == 9 {
            i = b;
            break;
        } else if batteries[b] > batteries[i] {
            i = b
        }
    }
    ret += batteries[i];

    return ret;
}

fn main() {
    let path = get_path();
    let data = match get_data(&path) {
        Err(e) => panic!("could not get data due to error: {}", e),
        Ok(data) => data,
    };

    let mut score = 0u64;
    for batteries in data {
        let j = find_largest_joltage(&batteries);
        // println!("{:?} = {}", batteries, j);
        score += j as u64;
    }

    println!("score={}", score)
}
