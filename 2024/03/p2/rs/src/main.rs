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

    let content = std::fs::read_to_string(path).expect("could not read file content");

    let mut ret = Vec::<Vec<usize>>::new();

    let ranges = content.match_indices("mul(")
                        .map(|(i, _)| i)
                        .chain([content.len()])
                        .collect::<Vec<usize>>()
                        .windows(2)
                        .map(|i| (i[0]+4, i[1]))
                        .collect::<Vec<(usize, usize)>>();

    let mut states = content.match_indices("do()")
                            .map(|(i, _)| (i, true))
                            .chain(content.match_indices("don't()")
                                          .map(|(i, _)| (i, false)))
                            .collect::<Vec<(usize, bool)>>();
    states.sort_by(|a, b| b.0.cmp(&a.0));

    let chars = content.chars().collect::<Vec<char>>();

    let mut next_state_index: usize = 0;
    let mut next_state_value: bool = true;
    let mut curr_state_value: bool = true;

    for (start, mut stop) in ranges {
        if start >= next_state_index {
            curr_state_value = next_state_value;
            if let Some((ni, nv)) = states.pop() {
                next_state_index = ni;
                next_state_value = nv;
            }
        }

        if !curr_state_value {
            continue;
        }

        if stop - start > 8 {
            stop = start + 8;
        }

        let mut numbers = Vec::<usize>::new();
        let mut length = 0usize;

        for ci in start..stop {
            if chars[ci].is_ascii_digit() {
                length += 1;
                continue;
            }

            if [',', ')'].contains(&chars[ci]) {
                if let 1..=3 = length {
                    if let Ok(val) = &content[ci-length..ci].parse::<usize>() {
                        numbers.push(*val);
                    }
                    length = 0;
                } else {
                    break;
                }
            }

            if chars[ci] == ')' {
                if numbers.len() > 1 {
                    ret.push(numbers);
                }
                break;
            }
            else if chars[ci] == ',' {
                continue;
            } else {
                break;
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
    println!("{}", separate_with_commas(&score));
}
