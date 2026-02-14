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

    let mut content: Vec<String> = Vec::new();

    for line in reader.lines() {
        line_no += 1;

        let data: String = match line {
            Err(e) => panic!("unable to read line {} => {}", line_no, e),
            Ok(s) => s
        };

        content.push(data);
    }

    let max_len = content.iter().map(|s| s.len()).max().expect("could not find max len of content");
    let op_line = content.pop().expect("no data");
    if content.is_empty() { panic!("no content") };

    let ops = ['+', '*'];
    let mut vals: Vec<usize> = Vec::new();
    let mut ret = Vec::new();
    for i in (0..max_len).rev() {
        let mut chars: Vec<char> = Vec::new();

        for r in 0..content.len() {
            if let Some(v) = content[r].chars().nth(i) {
                chars.push(v);
            }
        }

        if let Ok(v) = String::from_iter(chars).trim().parse::<usize>() {
            vals.push(v);
        }

        if let Some(op) = op_line.chars().nth(i) && ops.contains(&op) {
            ret.push(Col {
                nums: vals.drain(..).collect(),
                op: op.to_string()
            });
        }
    }

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
