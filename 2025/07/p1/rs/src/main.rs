use std::collections::HashSet;
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
    let mut line_no = 0;

    let mut ret: Vec<Vec<usize>> = Vec::new();

    for line in reader.lines() {
        line_no += 1;

        let data: String = match line {
            Err(e) => panic!("unable to read line {} => {}", line_no, e),
            Ok(s) => s
        };

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
    let mut beams: HashSet<usize> = HashSet::new();
    let mut data_iter = data.iter();
    if let Some(first) = data_iter.next() {
        beams.extend(first);
    } else {
        panic!("no data");
    }


    while let Some(pos) = data_iter.next() {
        for p in pos {
            if beams.contains(&p) {
                beams.extend([p-1, p+1]);
                beams.remove(p);
                result += 1;
            }
        }
    }

    println!("splits={:?}", format_usize(&result));
}
