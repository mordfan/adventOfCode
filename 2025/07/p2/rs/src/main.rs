use std::collections::HashMap;
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

    let mut ret: Vec<Vec<usize>> = Vec::new();

    for line in reader.lines() {
        let data: String = line.expect("unable to read line");
        let markers = ['S', '^'];
        let indices = data.char_indices()
                          .filter_map(|(i, c)| if markers.contains(&c) { Some(i) } else { None })
                          .collect::<Vec<usize>>();

        if !indices.is_empty() {
            ret.push(indices);
        }
    }

    return Ok(ret);
}

/// Returns formatted `usize` as `String` with thousand separator.
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
    let data = get_data(&path).expect("could not get data due to error");

    let width: usize = data.iter()
                           .map(|i| i.iter().max().expect("could not obtain max value"))
                           .max()
                           .expect("could not obtain max value") + 2; //+2 to accomodate bottom
                                                                      //left and bottom right beams
    let mut data_iter = data.iter();
    //current beam position with it's actual counter that represents possible paths number to get
    //to this spot
    let mut beams: HashMap<usize, usize> = HashMap::from_iter((0..width).map(|i| (i, 0)));
    if let Some(first) = data_iter.next() &&
       let Some(start) = first.first() &&
       let Some(b) = beams.get_mut(start) {
        *b = 1;
    } else {
        panic!("no data");
    }

    while let Some(splitters) = data_iter.next() {
        for p in splitters {
            let current_value = beams[&p];

            if current_value == 0 { continue; } // 0 means that no paths leads here

            if let Some(left) = beams.get_mut(&(p - 1)) {
                *left += current_value;
            }

            if let Some(right) = beams.get_mut(&(p + 1)) {
                *right += current_value;
            }

            if let Some(current) = beams.get_mut(&p) {
                *current = 0
            }

        }
    }

    let result: usize = beams.values().sum();
    println!("ways={:?}", format_usize(&result));
}
