use std::fs::File;
use std::io::{BufRead, BufReader};
use std::path::PathBuf;

#[derive(Debug)]
struct Col {
    nums: Vec<usize>,
    op: String
}

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

fn get_data(path: &PathBuf) -> Result<Vec<Col>, Box<dyn std::error::Error>> {
    println!("opening {:?}", path.canonicalize());

    let file = File::open(&path)?;
    let reader = BufReader::new(file);
    let mut line_no = 0;

    let mut nums: Vec<Vec<usize>> = Vec::new();
    let mut ops: Vec<String> = Vec::new();

    for line in reader.lines() {
        line_no += 1;

        let data: String = match line {
            Err(e) => panic!("unable to read line {} => {}", line_no, e),
            Ok(s) => s
        };

        //parse data
        let values: Vec<&str> = data.split_whitespace().collect();

        if let Some(first) = values.first() {
            if let Ok(_) = first.parse::<usize>() {
                //numbers
                nums.push(values.iter()
                                .map(|n| n.parse::<usize>().unwrap_or_else(|_| panic!("could not parse value to number")))
                                .collect::<Vec<usize>>());
            } else {
                //ops
                ops = values.iter().rev().map(|s| s.to_string()).collect();
            }
        }
    }

    //rotate numbers 90 degrees
    let rows = nums.len();
    let cols = nums.iter()
                   .map(|f| f.len())
                   .max()
                   .unwrap_or(0);
    let mut rotated = vec![vec![0; rows]; cols];
    for r in 0..rows {
        for c in 0..cols {
            rotated[cols - 1 - c][r] = nums[r][c];
        }
    }

    //combine nums and ops into output struct
    let ret: Vec<Col> = rotated.into_iter()
                               .zip(ops)
                               .map(|(nums, op)| Col { nums, op })
                               .collect();

    return Ok(ret);
}

#[allow(dead_code)]
fn format_usize(num: &usize) -> String {
    return num.to_string()
              .as_bytes()
              .rchunks(3)
              .rev()
              .map(std::str::from_utf8)
              .collect::<Result<Vec<&str>, _>>()
              .unwrap()
              .join(",");
}

fn main() {
    let path = get_path();

    let data = match get_data(&path) {
        Err(e) => panic!("could not get data due to error: {}", e),
        Ok(data) => data
    };

    let mut result = 0usize;
    for d in data {
        result += match d.op.as_str() {
            "+" => d.nums.iter().sum::<usize>(),
            "*" => d.nums.iter().product::<usize>(),
            _ => panic!("unknown op")
        };
    }
    println!("{:?}", format_usize(&result));
}
