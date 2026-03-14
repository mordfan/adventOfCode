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

fn get_data(path: &PathBuf) -> Result<Vec<Vec<usize>>, Box<dyn std::error::Error>> {
    println!("opening {:?}", path.canonicalize());

    let file = File::open(&path)?;
    let reader = BufReader::new(file);
    let mut ret = Vec::<Vec<usize>>::new();

    for line in reader.lines() {
        let s = line.expect("could not read line");
        if s.len() == 0 { continue; }

        let indexes = s.match_indices("mul(")
                       .map(|(i, _)| i)
                       .chain([s.len()])
                       .collect::<Vec<usize>>();

        if indexes.len() <= 1 { continue; }

        let ranges = indexes.windows(2)
                            .map(|i| (i[0]+4, i[1]))
                            .collect::<Vec<(usize, usize)>>();

        let chars = s.chars().collect::<Vec<char>>();

        for (start, stop) in ranges {
            let mut numbers = Vec::<usize>::new();
            let mut length = 0usize;
            for i in start..stop {
                if chars[i].is_ascii_digit() {
                    length += 1;
                    continue;
                }

                if chars[i] == ',' || chars[i] == ')' {
                    if let 1..=3 = length {
                        if let Ok(val) = &s[i-length..i].parse::<usize>() {
                            numbers.push(*val);
                        }
                        length = 0;
                    } else {
                        break;
                    }
                }

                if chars[i] == ')' {
                    if numbers.len() > 1 {
                        ret.push(numbers);
                    }
                    break;
                }
            }
        }
    }

    return Ok(ret);
}

/// Returns formatted `usize` as `String` with thousand separator.
#[allow(dead_code)]
fn separate_with_commas(num: &usize) -> String {
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
    let data = get_data(&path).expect("could not get data due to error");

    let mut score = 0usize;
    for d in data {
        score += d.iter().product::<usize>();
    }

    println!("{:?}", separate_with_commas(&score));
}
