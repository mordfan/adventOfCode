use std::fs::File;
use std::io::{BufRead, BufReader};
use std::path::PathBuf;

struct Data {
    ranges: Vec<Range>,
    ids: Vec<usize>
}

struct Range {
    start: usize,
    end: usize
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

fn get_data(path: &PathBuf) -> Result<Data, Box<dyn std::error::Error>> {
    println!("opening {:?}", path.canonicalize());

    let file = File::open(&path)?;
    let reader = BufReader::new(file);
    let mut line_no = 0;
    let mut ranges: Vec<Range> = Vec::new();
    let mut ids: Vec<usize> = Vec::new();

    for line in reader.lines() {
        line_no += 1;

        let data: String = match line {
            Err(e) => panic!("unable to read line {} => {}", line_no, e),
            Ok(s) => s
        };

        if data.len() == 0 { continue; }

        //parse data
        let splitter_index: usize = match data.chars().position(|c| c == '-') {
            Some(index) => index,
            None => 0
        };

        if splitter_index == 0 {
            //id
            let id: usize = match data.parse::<usize>() {
                Err(e) => panic!("could not parse line to id {e}"),
                Ok(i) => i
            };
            ids.push(id);
        } else {
            //range
            let start: usize = match data[..splitter_index].parse::<usize>() {
                Err(e) => panic!("could not parse line to id {e}"),
                Ok(i) => i
            };
            let end: usize = match data[splitter_index+1..].parse::<usize>() {
                Err(e) => panic!("could not parse line to id {e}"),
                Ok(i) => i
            };
            ranges.push(Range { start, end });
        }

    }

    return Ok(Data {
        ranges: ranges,
        ids: ids,
    });
}

fn main() {
    let path = get_path();

    let Data { mut ranges, mut ids } = match get_data(&path) {
        Err(e) => panic!("could not get data due to error: {}", e),
        Ok(data) => data
    };

    //reduce overlaping ranges for pt2 as it will also help in pt1
    ranges.sort_by(|a, b| a.start.cmp(&b.start));
    let mut merged: Vec<Range> = Vec::new();
    for r in ranges {
        match merged.last_mut() {
            Some(last) => {
                //check if ranges overlaps
                if last.end >= r.start {
                    //since it's integer values +1 will ensure neighboring
                    //ranges to be merged together
                    last.start = last.start.min(r.start);
                    last.end = last.end.max(r.end);
                } else {
                    merged.push(r)
                }
            },
            _ => merged.push(r),
        }
    }

    //determine amount of fresh ids for pt1
    let mut fresh_counter: usize = 0;
    ids.sort();

    let mut range_iterator = merged.into_iter();
    let mut current_range = Range { start: 0, end: 0 };

    'main: for id in ids {
        if id > current_range.end {
            loop {
                current_range = match range_iterator.next() {
                    Some(range) => range,
                    _ => break 'main
                };
                if current_range.end >= id { break; }
            }
        }

        if id >= current_range.start && id <= current_range.end {
            fresh_counter += 1;
        }
    }

    println!("fresh_counter={:?}", fresh_counter);

}
