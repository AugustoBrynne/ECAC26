# Ground truth

Every modification made to the published dataset, and nothing else.

| file | one row per |
|---|---|
| `truth_cells.csv` | changed cell: `song_id`, `column`, `original_value`, `corrupted_value`, `original_is_missing`, `corrupted_is_missing`, `defect_code` |
| `truth_rows.csv` | added or removed row: `song_id`, `action`, `duplicate_of`, `defect_code`, `note` |
| `truth_media.csv` | altered file: `song_id`, `kind`, `path`, `defect_code`, `note` |
| `originals/` | untouched copy of every media file that was altered, and nothing else |

## Codes

| code | count | meaning |
|---|---|---|
| `A1` | 25 | Row duplicated exactly, identifiers included. |
| `A2` | 120 | Artist name spelled differently on some of the artist's rows. |
| `A3` | 90 | Title altered: whitespace, apostrophe, case, or an appended suffix. |
| `B1` | 180 | Duration removed. The probability of removal rises with the duration itself (MNAR). |
| `B2` | 220 | ActualYear removed. The probability of removal falls with the number of songs the artist has in the dataset (MAR, on an observed column). |
| `B3` | 150 | Genres removed. The probability of removal depends on the quadrant (MAR, on the target). |
| `B4` | 120 | Relevance removed uniformly at random among the rows where it was present (MCAR). This is the control. The draw was repeated until it showed no detectable association with the value removed or with the target, so that a test for MCAR has a clean negative to find. |
| `C1` | 60 | Duration rewritten in milliseconds. |
| `C2` | 25 | Duration rewritten in minutes. |
| `C3` | 70 | Sentinel code written in place of a value. |
| `C4` | 15 | ActualYear set to a year that has not happened. |
| `C6` | 40 | ActualYear set earlier than LowestYear. Each value is ordinary alone; the pair is impossible. |
| `C7` | 45 | A weight list given a different number of entries from its tag list. |
| `F` | 893 | Row removed, to subsample a class. |
| `H1` | 1 | An outlier that no univariate rule can see: both values are ordinary for their columns, and the combination is further from any real record than 99 % of real records are from their own nearest neighbour. |
| `H2` | 1 | The same, in a second pair of columns and on a different record. |
| `H3` | 1 | A duration longer than any track in the published dataset. |
| `H4` | 1 | A relevance score beyond the end of the scale. |
| `H5` | 1 | A year before the dataset begins. |

## What is not in here

**The audio was not modified.** Every mp3 is byte-identical to the file
published by the dataset authors. No audio defect was injected and none is
recorded here.

**The published dataset has its own defects**, and they are not ours to
record. Missing values, sentinel codes, near-empty columns, repeated
recordings under two identifiers, and a target that can be reconstructed
from other columns are all present in the original and appear in no file in
this folder. A defect absent from this record is not therefore absent from
the data; it means only that we did not put it there. The measured rates at
which the published data already shows each of the injected patterns are:

| pattern | rate in the published data |
|---|---|
| `A1` | 0.0000 |
| `A2` | 0.0000 |
| `C6` | 0.0000 |
| `C7` | 0.0000 |

Families not injected, because the published data already shows them at
a rate of 2% or more: `E1`, `E2`, `E3`, `E4`, `G1`.

**`av_values.csv` was not modified.** Neither were the quadrant labels.

## How this is meant to be used

This is a measuring instrument. A cleaning decision is justified by the
analysis that led to it; this folder tells you afterwards how well that
analysis worked, which is a different question and the more interesting one.
