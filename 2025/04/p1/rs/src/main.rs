use std::fs::File;
use std::collections::HashSet;
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

fn get_data<T>(path: &PathBuf, parser: &dyn Fn(&str) -> T) -> Result<Vec<T>, Box<dyn std::error::Error>> {
    println!("opening {:?}", path.canonicalize());

    let file = File::open(&path)?;
    let reader = BufReader::new(file);
    let mut line_no = 0;
    let mut ret = Vec::<T>::new();
    for line in reader.lines() {
        line_no += 1;

        let data: T = match line {
            Err(e) => panic!("unable to read line {} => {}", line_no, e),
            Ok(val) => parser(val.as_str()),
        };

        ret.push(data);
    }

    return Ok(ret);
}

fn parse_line(line: &str) -> Vec<bool> {
    return line.chars().map(|c| c == '@').collect::<Vec<bool>>();
}

fn main() {
    let path = get_path();
    let raw_data = match get_data(&path, &parse_line) {
        Err(e) => panic!("could not get data due to error: {}", e),
        Ok(data) => match data.len() {
            0 => panic!("no data read"),
            _ => data
        }
    };

    let surrounding: [(i16, i16); 8] = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1), (0, 1),
        (1, -1), (1, 0), (1, 1)
    ];
    let indices: HashSet<(i16, i16)> =
        raw_data.iter()
                .enumerate()
                .flat_map(|(row, cols)| cols.iter()
                                            .enumerate()
                                            .filter_map(move |(col, &val)| if val { Some(((row+1) as i16, (col+1) as i16)) } else { None }))
                .collect();

    let mut removable: usize = 0;
    for (row, col) in &indices {
        let coords: HashSet<(i16, i16)> = surrounding.iter().map(|(r, c)| (row+r, col+c)).collect();
        let existing: &HashSet<_> = &indices.intersection(&coords).collect();

        if existing.len() < 4 {
            removable += 1;
        }
    }

    println!("removable={removable}");
}
