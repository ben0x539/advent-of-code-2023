use std::fs;
use std::thread;
use std::io::{self, BufRead};
use std::sync::{Arc,Mutex};

struct Step<'a>(&'a str, &'a [usize], u64);
fn add<'a>(stack: &mut Vec<Step<'a>>, springs: &'a str, groups: &'a [usize], weight: u64) {
    for Step(s, g, w) in stack.iter_mut() {
        if *s == springs && *g == groups {
            *w += weight;
            return;
        }
    }

    stack.push(Step(springs, groups, weight));
}

fn count(springs: &str, groups: &[usize]) -> u64 {
    let mut stack = vec![Step(springs.trim_matches('.'), groups, 1)];
    let mut valid = 0;
    let mut max_stack_len = 0;
    while stack.len() > 0 {
        stack.sort_by_key(|Step(s, _, _)| s.len());
        max_stack_len = usize::max(max_stack_len, stack.len());
        let Step(springs, groups, weight) = stack.pop().unwrap();

        if groups.len() == 0 {
            if !springs.contains('#') {
                valid += weight;
            }
            continue;
        }

        let n = groups[0];
        if springs.len() < n {
            continue;
        }

        if !springs[..n].contains('.') && !(springs.len() >= n+1 && &springs[n..n+1] == "#") {
            add(&mut stack, &springs[usize::min(n+1, springs.len())..], &groups[1..], weight);
        }

        if &springs[0..1] != "#" {
            add(&mut stack, &springs[1..], groups, weight);
        }
    }
    //dbg!((springs, max_stack_len));

    valid
}

fn main() {
    let f = fs::File::open("../inputs/input-day-12.txt").unwrap();
    let sum = Arc::new(Mutex::new(0));
    let mut lines = Vec::new();
    for line in io::BufReader::new(f).lines() {
        let line = line.unwrap();
        let (springs, groups) = line.rsplit_once(" ").unwrap();
        let groups: Vec<usize> = groups.split(",")
            .map(|s| s.parse().unwrap())
            .collect();
        let springs = vec![springs; 5].join("?");
        let groups: Vec<usize> = groups.iter().cloned().cycle().take(groups.len()*5).collect();
        lines.push((springs, groups));
    }

    let mut threads = Vec::new();

    let lines = Arc::new(Mutex::new(lines));

    for _ in 0..16 {
        let sum = sum.clone();
        let lines = lines.clone();
        threads.push(thread::spawn(move || {
            loop {
                let work = {
                    let mut lines = lines.lock().unwrap();
                    //dbg!(lines.len());
                    lines.pop()
                };
                if work.is_none() {
                    return;
                }
                let (springs, groups) = work.unwrap();
                let n = count(&springs, &groups);
                //dbg!(springs, n);
                *sum.lock().unwrap() += n;
            }
        }));
    }

    for t in threads {
        t.join().unwrap();
    }

    dbg!(*sum.lock().unwrap());
}
