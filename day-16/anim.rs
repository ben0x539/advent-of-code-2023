#!/usr/bin/env cargo


//! ```cargo
//! [package]
//! edition = "2021"
//! [dependencies]
//! color-eyre = "0.5.7"
//! ```

use std::fmt;
use std::fs;
use std::io::{self, Write};
use std::mem;
use std::ops;
use std::thread;

use color_eyre::eyre::{Result, bail};

#[derive(Clone, Copy, Debug, PartialEq, PartialOrd, Eq, Ord)]
enum Tile {
    Empty,
    SplitterHorizontal,
    SplitterVertical,
    Mirror,
    MirrorBack,
}

impl fmt::Display for Tile {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        let c = match *self {
            Tile::Empty => ' ',
            Tile::SplitterHorizontal => '─',
            Tile::SplitterVertical => '│',
            Tile::Mirror => '╱',
            Tile::MirrorBack => '╲',
        };

        write!(f, "{c}")
    }
}

#[derive(Clone, Copy, Debug, PartialEq, Eq, PartialOrd, Ord)]
struct V2(i32, i32);

impl ops::Add for V2 {
	type Output = V2;

	#[inline]
	fn add(self, V2(x2, y2): V2) -> V2 {
		let V2(x1, y1) = self;
		V2(x1 + x2, y1 + y2)
	}
}

impl ops::Sub for V2 {
	type Output = V2;

	#[inline]
	fn sub(self, rhs: V2) -> V2 {
		self + -rhs
	}
}

impl ops::Neg for V2 {
	type Output = V2;

	#[inline]
	fn neg(self) -> V2 {
		let V2(x, y) = self;
		V2(-x, -y)
	}
}

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
struct M22(V2, V2);

impl ops::Mul<V2> for M22 {
	type Output = V2;

	fn mul(self, rhs: V2) -> V2 {
		let M22(V2(x1, y1), V2(x2, y2)) = self;
		let V2(x, y) = rhs;
		V2(x1 * x + y1 * y, x2 * x + y2 * y)
	}
}

const NORTH: V2 = V2(0, -1);
const WEST: V2 = V2(-1, 0);
const SOUTH: V2 = V2(0, 1);
const EAST: V2 = V2(1, 0);

#[derive(Clone, Debug, PartialEq, PartialOrd, Eq, Ord)]
struct Grid {
    tiles: Vec<Tile>,
    width: i32,
    height: i32,
}

impl ops::Index<V2> for Grid {
    type Output = Tile;
    fn index(&self, V2(x, y): V2) -> &Tile {
        &self.tiles[x as usize + y as usize * self.width as usize]
    }
}

impl Grid {
    fn parse(buf: &[u8]) -> Result<Grid> {
        fn update_width(width: &mut Option<i32>, w: i32) -> Result<()> {
            match width {
                None => *width = Some(w),
                &mut Some(width) => if width != w {
                    bail!("inconsistent line width, previously {width}, now {w}");
                }
            }
            Ok(())
        }

        let mut width = None;
        let mut tiles = Vec::new();
        let mut last_line_start = 0;
        for (i, &c) in buf.iter().enumerate() {
            match c as char {
                '.' => tiles.push(Tile::Empty),
                '|' => tiles.push(Tile::SplitterVertical),
                '-' => tiles.push(Tile::SplitterHorizontal),
                '/' => tiles.push(Tile::Mirror),
               '\\' => tiles.push(Tile::MirrorBack),
                '\n' => {
                    if i == 0 {
                        bail!("zero width line");
                    }
                    let w = i - last_line_start;
                    last_line_start = i + 1;
                    update_width(&mut width, w as i32)?;
                }
                _ => bail!("unexpected char {c}"),
            }
        }

        let w = buf.len() - last_line_start;
        if w != 0 {
            update_width(&mut width, w as i32)?;
        }

        let grid = match width {
            None => Grid { tiles, width: 0, height: 0 },
            Some(width) => {
                let height = tiles.len() as i32 / width;
                Grid { tiles, width, height }
            }
        };

        Ok(grid)
    }
}

#[derive(Clone, Copy, Debug, PartialEq, Eq, PartialOrd, Ord)]
struct Ray {
    pos: V2,
    dir: V2,
}

impl Ray {
    fn step(&mut self) {
        self.pos = self.pos + self.dir;
    }

    fn is_in_bounds(&self, grid: &Grid) -> bool {
        let &Ray { pos: V2(x, y), .. } = self;

        x >= 0 && x < grid.width
            && y >= 0 && y < grid.height
    }
}

struct Trace {
    grid: Vec<i32>,
    width: usize,
}

impl Trace {
    fn new_for(grid: &Grid) -> Trace {
        Trace {
            grid: vec![0; grid.width as usize * grid.height as usize],
            width: grid.width as usize,
        }
    }

    fn record(&mut self, Ray { pos: V2(x, y), dir: V2(dx, dy) }: Ray) -> bool {
        let r = &mut self.grid[x as usize + y as usize * self.width];
        let b =
            //match V2(dx, dy) {
            //    V2(0, -1) => 0b0001,
            //    V2(-1, 0) => 0b0010,
            //    V2(0, 1) =>  0b0100,
            //    V2(1, 0) =>  0b1000,
            //    _ => 0,
            //};
            (dx+3*dx*dx)/2 + (dy+3*dy*dy)*2;
        let new = b & *r == 0;

        *r |= b;

        new
    }

    fn check(&mut self, V2(x, y): V2) -> bool {
        self.grid[x as usize + y as usize * self.width] > 0
    }

    fn count(&self) -> i32 {
        self.grid.iter().cloned().filter(|&r| r > 0).count() as i32
    }
}

const TURN_RIGHT: M22 = M22(V2(0, 1), V2(-1, 0));
const MIRROR: M22 = M22(V2(0, -1), V2(-1, 0)); // /
const MIRROR_BACK: M22 = M22(V2(0, 1), V2(1, 0)); // \


fn trace(grid: &Grid, pos: V2, dir: V2) -> i32 {
    let mut rays = vec![Ray { pos, dir }];
    let mut next_rays = vec![];
    let mut paths = Trace::new_for(grid);

    while rays.len() > 0 {
        for mut ray in rays.drain(..) {
            ray.step();

            if !ray.is_in_bounds(grid) {
                continue;
            }

            if !paths.record(ray) {
                continue;
            }

            match grid[ray.pos] {
                Tile::SplitterHorizontal if ray.dir.1 != 0 => {
                    ray.dir = TURN_RIGHT*ray.dir;
                    let r2 = Ray { pos: ray.pos, dir: -ray.dir };
                    if paths.record(r2) {
                        next_rays.push(r2);
                    }
                    if !paths.record(ray) {
                        continue;
                    }
                    //next_rays.push(r2);
                }
                Tile::SplitterVertical if ray.dir.0 != 0 => {
                    ray.dir = TURN_RIGHT*ray.dir;
                    let r2 = Ray { pos: ray.pos, dir: -ray.dir };
                    if paths.record(r2) {
                        next_rays.push(r2);
                    }
                    if !paths.record(ray) {
                        continue;
                    }
                    //next_rays.push(r2);
                }
                Tile::Mirror => ray.dir = MIRROR*ray.dir,
                Tile::MirrorBack => ray.dir = MIRROR_BACK*ray.dir,
                _ => {}
            }

            next_rays.push(ray);
        }

        mem::swap(&mut rays, &mut next_rays);
        rays.sort();
        rays.dedup();

        let mut buf = Vec::new();
        //_ = write!(&mut buf, "\x1b[2J");
        for y in 0..grid.height {
            for x in 0..grid.width {
                let p = V2(x, y);
                let c = grid[p];
                if rays.iter().any(|r| r.pos == p) {
                    //_ = write!(&mut buf, "∗");
                    _ = write!(&mut buf, "\x1b[103m∗\x1b[0m");
                } else if c == Tile::Empty && paths.check(p) {
                    //_ = write!(&mut buf, "·");
                    _ = write!(&mut buf, "\x1b[93m·\x1b[0m");
                } else {
                    //_ = write!(&mut buf, "{}", grid[p]);
                    _ = write!(&mut buf, "{}", grid[p]);
                }
            }
            _ = writeln!(&mut buf, "");
        }
        _ = writeln!(&mut buf, "");
        _ = writeln!(&mut buf, "");
        {
            let mut stdout = io::stdout();
            _ = stdout.write(&buf);
            _ = stdout.flush();
        }
        #[allow(deprecated)]
        thread::sleep_ms(20);
    }

    //for y in 0..grid.height {
    //    for x in 0..grid.width {
    //        let n = paths.grid[x as usize + y as usize * paths.width];
    //        let c = if n == 0 { ' ' } else { '#' };
    //        print!("{c}");
    //    }
    //    println!();
    //}

    return paths.count();
}

fn main() -> Result<()> {
    color_eyre::install()?;

    let grid = Grid::parse(&fs::read("../inputs/input-day-16.txt")?)?;
    //dbg!(grid.width, grid.height);
    let energized = trace(&grid, V2(-1, 0), EAST);
    //dbg!(energized);
    Ok(())
}
