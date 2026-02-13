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

fn parse_line(line: &str) -> Vec<usize> {
    return line.chars()
               .enumerate()
               .filter_map(|(i, c)| if c == '@' { Some(i) } else { None } )
               .collect();
}

fn main() {
    let path = get_path();

    let data = match get_data(&path, &parse_line) {
        Err(e) => panic!("could not get data due to error: {}", e),
        Ok(data) => match data.len() {
            0 => panic!("no data read"),
            _ => data
        }
    };

    //+1 to both row and col to make up for empty top row and left col
    let coords: Vec<(usize, usize)> =
        data.iter()
            .enumerate()
            .flat_map(|(row, cols)| cols.iter().map(move |col| return (row+1, *col+1)))
            .collect();

    let mut state: HashMap<(usize, usize), bool> =
        coords.iter()
              .map(|&key| (key, true))
              .collect();

    let mut removed: usize = 0;
    let mut changed = true;

    while changed {
        changed = false;
        for key in &coords {
            if let Some(value) = state.get(&key) {
                if *value == false { continue; }
            } else {
                continue;
            }

            let (row, col) = key;
            let mut adj = 0u8;

            //row above
            if let Some(occupied) = state.get(&(row-1, col-1)) && *occupied { adj += 1; }
            if let Some(occupied) = state.get(&(row-1, col+0)) && *occupied { adj += 1; }
            if let Some(occupied) = state.get(&(row-1, col+1)) && *occupied { adj += 1; }
            //same row
            if let Some(occupied) = state.get(&(row+0, col-1)) && *occupied { adj += 1; }
            if let Some(occupied) = state.get(&(row+0, col+1)) && *occupied { adj += 1; }
            //row below
            if let Some(occupied) = state.get(&(row+1, col-1)) && *occupied { adj += 1; }
            if let Some(occupied) = state.get(&(row+1, col+0)) && *occupied { adj += 1; }
            if let Some(occupied) = state.get(&(row+1, col+1)) && *occupied { adj += 1; }

            if adj >= 4 { continue; }

            if let Some(value) = state.get_mut(&key) {
                *value = false;
                changed = true;
                removed += 1;
            }
        }
    }

    println!("removed={removed}");
}
