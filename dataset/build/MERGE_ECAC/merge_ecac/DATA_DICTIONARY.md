# Data dictionary

What each column of `metadata.csv` is **intended** to contain. This file
describes the intent of the people who built the table. It is not a guarantee
about the file you have, and checking the file against this description is the
first thing worth doing.

| column | intended content |
|---|---|
| `Audio_Song` | Identifier of the audio excerpt. One row per identifier; the identifier matches a file in `audio/<Quadrant>/`. |
| `Lyric_Song` | Identifier of the lyrics file, matching a file in `lyrics/<Quadrant>/`. |
| `Quadrant` | Target variable. Quadrant of Russell's circumplex: `Q1` high arousal and high valence, `Q2` high arousal and low valence, `Q3` low arousal and low valence, `Q4` low arousal and high valence. |
| `AllMusic Id` | Track identifier in the AllMusic catalogue. |
| `AllMusic Extraction Date` | Which of the two collection runs produced the record: `Old` or `New`. |
| `Artist` | Performing artist. One spelling per artist, used consistently across that artist's rows. |
| `Title` | Track title as published. |
| `Relevance` | Score returned by AllMusic for the query that retrieved the track. Positive real number. |
| `Year` | Release date as recorded by AllMusic, in `YYYY-MM-DD` form, with unknown components written as `??`. |
| `LowestYear` | Earliest release date found for the track, in `DD/MM/YYYY` form. Never later than `ActualYear`. |
| `Duration` | Duration of the complete track in seconds. Greater than zero. |
| `Moods` | Mood tags from the reduced AllMusic vocabulary, comma separated. |
| `MoodsAll` | Mood tags from the complete AllMusic vocabulary, comma separated. |
| `MoodsAllWeights` | One weight per tag in `MoodsAll`, in the same order and in the same number. |
| `Genres` | Genre tags, comma separated. |
| `GenreWeights` | One weight per tag in `Genres`, same order, same number. |
| `Themes` | Theme tags, comma separated. |
| `ThemeWeights` | One weight per tag in `Themes`, same order, same number. |
| `Styles` | Style tags, comma separated. |
| `StyleWeights` | One weight per tag in `Styles`, same order, same number. |
| `AppearancesTrackIDs` | AllMusic identifiers of other appearances of the same recording. |
| `AppearancesAlbumIDs` | Album identifier for each entry of `AppearancesTrackIDs`, same order, same number. |
| `Sample` | Whether a 30-second sample was available at collection time. |
| `SampleURL` | Address the excerpt was retrieved from. |
| `ActualYear` | Release year used by the dataset authors. Four digits, not in the future. |
| `num_Genres` | Number of genre tags for the track. |
| `num_MoodsAll` | Number of mood tags for the track. |

`av_values.csv` carries `Arousal` and `Valence` for each song, on a scale from
0 to 1, keyed by `Audio_Song` and `Lyric_Song`.

## Folders

| folder | contents |
|---|---|
| `audio/` | One mp3 excerpt of 30 seconds per song, under the song's quadrant. |
| `lyrics/` | One plain text file per song, under the song's quadrant. |
| `album_covers/` | One jpeg per song, where a cover could be retrieved. Not every song has one. |

These three folders sit beside `merge_ecac/`, not inside it.

The media folders were assembled independently of the table. Whether every row
has a file, and every file a row, is a property of this particular package and
not something the folders guarantee.
