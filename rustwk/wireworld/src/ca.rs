#[derive(Debug, Copy, Clone, PartialEq, Eq)]
pub enum Cell {
    Blank,
    Head,
    Tail,
    Copper,
}

pub struct Wireworld {
    pub grids: Vec<Vec<Cell>>,
    pub page: usize,
    pub stride: usize,
    pub offset: usize,
    pub rows: usize,
    pub cols: usize,
}

impl Wireworld {
    pub fn new(rows: usize, cols: usize) -> Wireworld {
        let size = (rows + 2) * (cols + 2);
        Wireworld {
            grids: vec![
                (0..size).map(|_| Cell::Blank).collect(),
                (0..size).map(|_| Cell::Blank).collect(),
            ],
            page: 0,
            stride: cols + 2,
            offset: cols + 3,
            rows,
            cols,
        }
    }

    pub fn step(&mut self) {
        let nextpage = (self.page + 1) % self.grids.len();
        for row in 0..(self.rows as isize) {
            for col in 0..(self.cols as isize) {
                let idx = self.idx(row, col);
                let next = match self.grids[self.page][idx] {
                    Cell::Blank => Cell::Blank,
                    Cell::Head => Cell::Tail,
                    Cell::Tail => Cell::Copper,
                    Cell::Copper => match self.neighbor_headcount(idx) {
                        1 | 2 => Cell::Head,
                        _ => Cell::Copper,
                    },
                };
                self.grids[nextpage][idx] = next;
            }
        }
        self.page = nextpage;
    }

    pub fn idx(&self, row: isize, col: isize) -> usize {
        self.offset + (row as usize) * self.stride + (col as usize)
    }

    pub fn get(&self, row: isize, col: isize) -> Cell {
        self.grids[self.page][self.idx(row, col)]
    }

    pub fn set(&mut self, row: isize, col: isize, to: Cell) {
        let idx = self.idx(row, col);
        self.grids[self.page][idx] = to;
    }

    fn neighbor_headcount(&self, idx: usize) -> usize {
        let mut count = 0;
        for i in [
            idx - self.stride - 1,
            idx - self.stride + 1,
            idx + self.stride - 1,
            idx + self.stride + 1,
            idx - self.stride,
            idx + self.stride,
            idx - 1,
            idx + 1,
        ] {
            count += match self.grids[self.page][i] {
                Cell::Head => 1,
                _ => 0,
            }
        }
        count
    }
}

#[test]
fn test_ca_diode() {
    // 0 1 2 3 4 5 6 7 8
    // . . . . . . . . . 0
    // . . . . O O . . . 1
    // . O ~ # . O O O . 2
    // . . . . O O . . . 3
    // . . . . . . . . . 4
    // . . . . O O . . . 5
    // . O ~ # O . O O . 6
    // . . . . O O . . . 7
    // . . . . . . . . . 8

    fn diode_die(ww: &mut Wireworld, row: isize, col: isize) {
        // center bit
        for i in 0..7 {
            ww.set(row + 1, col + i, Cell::Copper);
        }

        // two "ears"
        ww.set(row, col + 3, Cell::Copper);
        ww.set(row, col + 4, Cell::Copper);
        ww.set(row + 2, col + 3, Cell::Copper);
        ww.set(row + 2, col + 4, Cell::Copper);
    }

    fn assert_all_heads_in_row(ww: &Wireworld, row_expect: usize) {
        for row in 0..ww.rows {
            for col in 0..ww.cols {
                match ww.get(row as isize, col as isize) {
                    Cell::Head => assert_eq!(row_expect, row),
                    _ => (),
                }
            }
        }
    }

    fn assert_all_heads_in_col(ww: &Wireworld, col_expect: usize) {
        for row in 0..ww.rows {
            for col in 0..ww.cols {
                match ww.get(row as isize, col as isize) {
                    Cell::Head => assert_eq!(col_expect, col),
                    _ => (),
                }
            }
        }
    }

    let mut ww = Wireworld::new(9, 9);

    // first diode, should block the electron
    diode_die(&mut ww, 1, 1);
    ww.set(2, 2, Cell::Tail);
    ww.set(2, 3, Cell::Head);
    ww.set(2, 4, Cell::Blank);

    // second diode, should pass the electron
    diode_die(&mut ww, 5, 1);
    ww.set(6, 2, Cell::Tail);
    ww.set(6, 3, Cell::Head);
    ww.set(6, 5, Cell::Blank);

    // check that the electrons move as expected
    assert_all_heads_in_col(&ww, 3);
    ww.step();
    assert_all_heads_in_col(&ww, 4);
    ww.step();
    assert_all_heads_in_col(&ww, 5);
    ww.step();
    assert_all_heads_in_col(&ww, 6);
    assert_all_heads_in_row(&ww, 6);
}
