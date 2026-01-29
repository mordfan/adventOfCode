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

fn find_largest_joltage(batteries: &Vec<u8>, cnt: usize) -> u64 {
    let mut ret = 0u64;
    let mut cur = 0usize;

    for n in 0..cnt {
        let mut val = &0u8;
        let max = &batteries.len() - cnt + n + 1;
        for i in cur..max {
            if &batteries[i] > &val {
                cur = i;
                val = &batteries[i];
                if val == &9 {
                    break;
                }
            }
        }
        ret += (*val as u64) * u64::pow(10, (cnt - n - 1) as u32);
        cur += 1;
    }

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
        let j = find_largest_joltage(&batteries, 12);
        score += j as u64;
    }

    println!("score={}", format!("{:}", score));
}
