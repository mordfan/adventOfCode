use std::fs::File;
use std::io::{BufRead, BufReader};
use std::path::PathBuf;

struct Data {
    ranges: Vec<Range>,
    #[allow(dead_code)]
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

    let Data { mut ranges, .. } = match get_data(&path) {
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

    let fresh_counter = merged.iter().map(|r| r.end - r.start + 1).sum::<usize>();


    println!("fresh_counter={:?}", format_usize(&fresh_counter));

}
