# TglStemmer

**A Python library for Tagalog word stemming.**


## About

[tglstemmer](src/tglstemmer/) reduces all forms of Tagalog-inflected words, which can include out-of-vocabulary (OOV) words and Tagalog-English (Taglish) intrawords, to their base or root. It uses iterative and combinative affix removal, reduplication reduction, and application of transformation rules to derive candidates or possible stems of the word. The list of candidates is filtered based on a list of valid words and acceptability conditions. The best candidate is then chosen based on affix and reduplication length and number of contraction and transformation occurrences.


## Installation

To install the latest development version from GitHub, use:

```bash
pip install git+https://github.com/andrianllmm/tagalog-stemmer.git@main
```


## Usage

tglstemmer acts as a standalone library that can be imported via `from tglstemmer import stemmer`.

To get the stem of a word use the function `get_stem()`. This takes a word and returns its stem as a `Stem` object (basically a string with affixes, reduplication, transformations, etc. as additional attributes)
```python
stem = stemmer.get_stem("nagsulat")
print(stem)
# Output: 'sulat'
```

Since `get_stem` returns a `Stem` object, the affixes, reduplication, transformations, etc. used in the stemming process can be accessed as attributes.
```python
prefix = stem.pre
print(prefix)
# Output: 'nag'

suffix = stem.suf
print(suffix)
# Output: None
```

To get the stem of each word in a text use the function `get_stems()`. This takes a text and returns the stem of each word as a list of `Stem` objects.
```python
stems = stemmer.get_stems("nagsulat, binasa, at punitin")
print(stems)
# Output: ['sulat', 'basa', 'at', 'punit']
```

To get all the stem candidates of a word use the function `get_stem_candidates`. This takes a word and returns the possible stems as a list of `Stem` objects. This is helpful for loose checking considering candidate selection is not perfect.
```python
candidates = stemmer.get_stem_candidates("pinakamahusay't")
print(candidates)
# Output: ['husay', 'mahusay', 'pinakamahusay']
```


## Accuracy

The accuracy of tglstemmer was tested using a list of stems and their corresponding inflection. The list is manually derived from the examples from the book [Balarila ng Wikang Pambansa (Santos, 1939)](https://tl.wikipedia.org/wiki/Balarila_ng_Wikang_Pambansa), particularly in sections "Palabuuan ng mga Salita" (pp. 28-34) and "Mga Sangkap ng Pananalita" (pp. 35-37). This is not a "gold" standard dataset but is chosen for testing as the book gives varying examples of inflections as it discusses the process of affixation. Each inflection was stemmed by tglstemmer and then compared to the original stem. The test included 266 stem-inflection pairs.

| Metric | Value |
|---|---|
| Accuracy | 75.19% |
| Correct Attempts | 200 |
| Incorrect Attempts | 66 |
| Understemming Avg | 0.69 |
| Overstemming Avg | 0.12 |
| Understemming Total | 184 |
| Overstemming Total | 33 |


## Issues

* List of valid words: The default list of valid words is from the [Pinoy dictionary website](https://tagalog.pinoydictionary.com) which is an unreliable source for Tagalog root words since it lacks even some common words and contains inflected words.
* List of affixes: The list of affixes used is supplied by common affixes and manually combining them which is unreliable it lacks a reliable source.
* Test dataset: The dataset used in testing is limited and manually encoded from a book.
* Candidate selection: The process for selecting the best candidate can be further optimized to reduce stemming errors.

If you encounter any issues or bugs, please report them on the [GitHub issues page](#).


## Contributing

This project welcomes contributions and suggestions. Please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.


## License

This project is licensed under the [GPL-3.0 License](LICENSE).

---

For more information contact [maagmaandrian@gmail.com](mailto:maagmaandrian@gmail.com) with any additional questions or comments.