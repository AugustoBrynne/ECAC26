# Class distribution of this dataset

The quadrant distribution of this dataset is not the distribution of the
published MERGE Bimodal Complete dataset. Two classes were subsampled on
purpose, before any other modification, and the rows removed are listed in
`truth/truth_rows.csv` with the code `F`.

| quadrant | in the published dataset | kept here | fraction |
|---|---|---|---|
| Q1 | 525 | 525 | 1.00 |
| Q2 | 673 | 168 | 0.25 |
| Q3 | 500 | 500 | 1.00 |
| Q4 | 518 | 130 | 0.25 |

Total rows after subsampling: **1323**. Largest class over smallest:
**4.04:1**. A classifier that always answers with the majority
class is right **39.7%** of the time.

The subsampling is uniformly at random within each class, with a fixed seed.
It is not stratified by artist, by year or by anything else, so the group
structure of the surviving rows is the group structure of the original.

## Two things to notice before using this

The two subsampled classes were not chosen for convenience. One of them is
well separated from the rest of the data and the other overlaps heavily with
a neighbour. They are scarce to the same degree. What happens to them is not
the same, and the difference is the point.

Second: with a test partition of 15 % the smallest class contributes about
20 examples to it. Any per-class figure computed on that many
examples carries an interval wide enough to matter, and reporting the figure
without the interval would be a mistake.

The complete, unsubsampled table is available in `merge_original/metadata.csv`.
