# TglStemmer

**A Python library for Tagalog word stemming**

## About

TglStemmer is a library that finds the root form of
<a href="https://www.ethnologue.com/language/tgl" target="_blank">Tagalog</a>
words. It works on inflected words, even those with mixed Tagalog-English
(Taglish) terms or those not found in dictionaries. It removes affixes, reduces
repeated syllables, and applies transformation rules to find possible root
forms. These are filtered using a list of valid words and conditions. The best
root is then chosen based on how much was changed during the process.

## Installation

```sh
pip install tglstemmer
```

## Usage

TglStemmer acts as a standalone library that can be imported via
`from tglstemmer import stemmer`.

Use `get_stem` to get the root of a word. This takes a word and returns its stem
as a `Stem` object (basically a string with affixes, reduplication,
transformations, etc. as additional attributes).

```python
stem = stemmer.get_stem("nagsulat")
print(stem)
# Output: 'sulat'
```

Since `get_stem` returns a `Stem` object, the properties used in the stemming
process can be accessed as attributes.

```python
prefix = stem.pre
print(prefix)
# Output: 'nag'

suffix = stem.suf
print(suffix)
# Output: None
```

Use `get_stems()` to get the root of each word in a text. This takes a text and
returns the stem of each word as a list of `Stem` objects.

```python
stems = stemmer.get_stems("nagsulat, binasa, at punitin")
print(stems)
# Output: ['sulat', 'basa', 'at', 'punit']
```

Use `get_stem_candidates` to get all the stem candidates of a word. This takes a
word and returns the possible stems as a list of `Stem` objects. This is helpful
for loose checking considering candidate selection is not perfect.

```python
candidates = stemmer.get_stem_candidates("pinakamahusay't")
print(candidates)
# Output: ['husay', 'mahusay', 'pinakamahusay']
```

## Accuracy

The accuracy was tested using a list of stems and their corresponding
inflections. The list is manually derived from the examples from the book
[Balarila ng Wikang Pambansa (Santos, 1939)](https://tl.wikipedia.org/wiki/Balarila_ng_Wikang_Pambansa),
particularly in sections "Palabuuan ng mga Salita" (pp. 28-34) and "Mga Sangkap
ng Pananalita" (pp. 35-37). This is not a "gold" standard dataset but is chosen
for testing as the book provides varied examples of inflections during its
discussion about the process of affixation. Each inflection was stemmed by
TglStemmer and then compared to the original stem. The test included 266
stem-inflection pairs.

| Metric              | Value  |
| ------------------- | ------ |
| Accuracy            | 75.19% |
| Correct Attempts    | 200    |
| Incorrect Attempts  | 66     |
| Understemming Avg   | 0.69   |
| Overstemming Avg    | 0.12   |
| Understemming Total | 184    |
| Overstemming Total  | 33     |

## Development

This project uses [uv](https://docs.astral.sh/uv/) for dependency management.

Clone the repo and sync dependencies (including dev and test groups):

```sh
git clone https://github.com/andrianllmm/tagalog-stemmer.git
cd tagalog-stemmer
uv sync --all-groups
```

Run the tests:

```sh
uv run pytest
```
