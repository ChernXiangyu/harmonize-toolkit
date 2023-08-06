## Packages

This package contains several modules for text preprocessing and natural language processing (NLP). Here's an overview of each module and its functionality:

### preprocess.py

This module provides functions for preprocessing text data. The functions included are:

- `isGoodKw(keyword: str, length: int = 5, size: int = 2, exclude_strings: list = [])`: This function filters keywords based on length, size, and excluded strings.

- `removeBadSubstring(string: str, bad_string_list: list) -> str`: This function removes specified substrings from a given string.

- `removeBadWord(string: str, bad_word_list: list) -> str`: This function removes specified individual words from a given string.

- `removeShortWord(string: str)`: This function removes short words (length 1) from a given string.

- `remove_duplicates(input_list: list) -> list`: This function removes duplicate elements from a list.

- `remove_symbols(text)`: This function removes specified symbols from a given text using regular expressions.

- `preprocessString(string: str) -> str`: This function preprocesses a string by removing tone marks, converting it to lowercase, and cleaning up whitespace.

- `processedPublication(string: str)`: This function preprocesses a publication name by converting it to lowercase, removing symbols, replacing numeric symbols with empty strings, removing bad substrings and words, removing short words, and stripping whitespace.

### keywordGenerator.py

This module provides functions for generating keywords from strings and matching them with other strings. The functions included are:

- `getStringIntersectionList(stringList: list)`: This function finds the common words among a list of strings.

- `getKeyword(strings: list, scorer=fuzz.token_sort_ratio, score_cutoff=90)`: This function generates keywords from a list of strings using fuzzy matching and common word extraction techniques.

- `is_subsequence(keywordList, targetString)`: This function checks if a list of words appears in order in a target string.

- `matchKeyword(keywords: list, strings, process_function=processedPublication)`: This function matches keywords with strings based on word order and similarity.

### nlp.py

This module uses the spaCy library for natural language processing (NLP) tasks. The functions included are:

- `extract_organizations(string: str)`: This function extracts organizations from a given string using spaCy's NLP pipeline.

- `extract_persons(string: str)`: This function extracts persons (names) from a given string using spaCy's NLP pipeline.

- `extract_gpes(string: str)`: This function extracts GPEs (Geopolitical Entities) from a given string using spaCy's NLP pipeline.

- `analyze_entity(entity: str)`: This function analyzes entities (persons, organizations, and GPEs) from a given string using spaCy's NLP pipeline.

- `analyze_entities(entities: list)`: This function analyzes entities from a list of strings using spaCy's NLP pipeline.

### Dependencies

The following external dependencies are required for these modules to work:

- `pandas`: A library for data manipulation and analysis.
- `rapidfuzz`: A library for fuzzy string matching.
- `tqdm`: A library for creating progress bars.
- `spacy`: A library for NLP.

Make sure to install these dependencies before using the package.

### Usage

To use these modules, import the desired functions from the respective modules in your Python script. You can then call the functions with the appropriate input to perform text preprocessing or NLP tasks.

Please refer to the documentation and function descriptions within each module for detailed information on the input parameters and return values of each function.

