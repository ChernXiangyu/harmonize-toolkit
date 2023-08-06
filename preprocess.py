import re
import unicodedata
from collections import Counter
import pandas as pd
from rapidfuzz import fuzz
import json

def split_string(text, spliters: str):
    # 使用所有标点符号作为分隔符

    for spliter in spliters:
        text = text.replace(spliter, '#')  # 将标点符号替换为#
    # 使用空格作为分隔符拆分字符串
    split_list = text.split('#')
    return split_list

def has_consecutive_digits(string, n=2):
    pattern = r"\d{" + str(n) + r",}"
    matches = re.findall(pattern, string)
    return bool(matches)

def remove_consecutive_digits(string, n=2, replacement=''):
    pattern = r"\d{" + str(n) + r",}"
    result = re.sub(pattern, replacement, string)
    return result

def isGoodKw(keyword: str, length: int = 5, size: int = 2, exclude_strings: list = []):
    '''Keyword filter, only reserve keyword that...'''
    kw_list = keyword.split()
    if len(keyword) <= length or len(kw_list) <= size:
        return False
    # Contains excluded strings
    if any(exclude_str in keyword for exclude_str in exclude_strings):
        return False
    
    return True


def removeBadSubstring(string: str, bad_string_list: list) -> str:
    for bad_string in bad_string_list:
        string = string.replace(bad_string, '')
    return string

def removeBadWord(string: str, bad_word_list: list) -> str:
    word_list = string.split()
    for bad_word in bad_word_list:
        if bad_word in word_list:
            word_list.remove(bad_word)
    string = ' '.join(word_list)
    return string

def removeShortWord(string: str, lower_bound_len=2):
    word_list = string.split()
    word_list = [word for word in word_list if len(word) >= lower_bound_len]
    string = ' '.join(word_list)
    return string

def remove_duplicates(input_list):
    return list(dict.fromkeys(input_list))

def remove_symbols(text, replacement=' '):
    symbols = ['!', ',', '?', '(', ')', '-', '_', '\\', '/', '.', '"', "'", '[', ']', ':', '…', ';', '’', '“', '–', '=', '&', '{', '}', '&', '·']
    pattern = '[' + re.escape(''.join(symbols)) + ']'
    result = re.sub(pattern, replacement, text)
    return result

def remove_punctuation(string):
    normalized_string = unicodedata.normalize('NFD', string)  # 规范化字符串
    result = ''.join(char for char in normalized_string if not unicodedata.category(char).startswith('P'))  # 去除标点符号
    return result

def removeDigits(string):
    pattern = r"\d"  # 匹配数字的正则表达式模式
    result = re.sub(pattern, "", string)  # 使用空字符串替换匹配到的数字
    return result


def extract_duplicates(lst):
    counter = Counter(lst)  # 使用 Counter 统计每个字符串的出现次数
    duplicates = [item for item, count in counter.items() if count > 1]  # 提取出现次数大于1的字符串
    return duplicates

def remove_inner_parentheses(input_string):
    return re.sub(r'\([^()]*\)', '', input_string)

import re

def replace_continuous_spaces(string):
    """
    将连续的空格替换为单个空格

    参数：
    string (str): 输入的字符串

    返回值：
    str: 替换连续空格后的字符串
    """
    # 使用正则表达式替换连续的空格为单个空格
    cleaned_string = re.sub(r"\s+", " ", string)
    return cleaned_string

def preprocessString(string: str, lower=True) -> str:
    '''Preprocesses a string by removing tone marks, converting to lowercase, and cleaning up whitespace.

    Args:
        string (str): The string to be preprocessed.

    Returns:
        str: The preprocessed string.
    '''

    string = remove_inner_parentheses(string)
    
    # Check input type
    if not isinstance(string, str):
        raise TypeError("Input must be a string")

    # Remove tone marks
    string = unicodedata.normalize('NFD', string)
    string = ''.join(c for c in string if unicodedata.category(c) != 'Mn')

    # Convert uppercase letters to lowercase
    if lower:
        string = string.lower()

    # Replace continuous space with a single space
    string = replace_continuous_spaces(string)

    # Strip leading and trailing whitespace
    processed_string = string.strip()

    # Return the processed string
    return processed_string

map = {}

def processedPublication(text: str):
    '''Preprocesses the publication name by converting it to lowercase and keeping only alphanumeric characters'''
    processed_text = text
    processed_text = preprocessString(processed_text)
    
    processed_text = remove_symbols(processed_text)
    # Replace numeric symbols with empty text
    processed_text = re.sub(r'[0-9]', '', processed_text)
    processed_text = removeBadSubstring(processed_text, bad_strings)
    # Replace continuous space with a single space
    processed_text = re.sub(r"\s+", " ", processed_text)
    processed_text = removeShortWord(processed_text)
    processed_text = removeBadWord(processed_text, useless_words)
    # strip
    processed_text = processed_text.strip()
    processed_text = removeBadWord(processed_text, roman_num)
    # Return the processed text
    return processed_text
    
def preprocessInstitute(text: str):
    word_list = preprocessString(text).split(';')
    word_list = [word.strip() for word in word_list]
    return word_list

def remove_employment_type(text: str):
    employment_types = ['full-time', 'part-time', 'contract', 'internship', 'self-mployed', 'full time', 'part time', 'fulltime', 'parttime']
    word_list = text.split()
    for word in word_list:
        if word.lower() in employment_types:
            word_list.remove(word)
    text = ' '.join(word_list)
    text = text.replace('·', '')
    text = text.strip()
    return text

def processEntity(text: str):
    text = unicodedata.normalize('NFD', text)
    text = remove_punctuation(text)
    text = remove_employment_type(text)
    text = preprocessString(text, lower=False)
    # Replace numeric symbols with a single space
    text = re.sub(r'[0-9]', ' ', text)
    # Replace continuous space with a single space
    text = re.sub(r"\s+", " ", text)
    # Strip leading and trailing whitespace
    text = text.strip()
    return text

def processSchool(text: str):

    pass

# -----------------------------------------------------------------------
numeric_strings = ['first', 'second', 'third', 'fourth', 'fifth', 'sixth', 'seventh', 'eighth', 'ninth', 'tenth',
                   'eleventh', 'twelfth', 'thirteenth', 'fourteenth', 'fifteenth', 'sixteenth', 'seventeenth', 'eighteenth', 'nineteenth', 'twentieth',
                   'twenty-first', 'twenty-second', 'twenty-third', 'twenty-fourth', 'twenty-fifth', 'twenty-sixth', 'twenty-seventh', 'twenty-eighth', 'twenty-ninth', 'thirtieth',
                   'thirty-first', 'thirty-second', 'thirty-third', 'thirty-fourth', 'thirty-fifth', 'thirty-sixth', 'thirty-seventh', 'thirty-eighth', 'thirty-ninth', 'fortieth',
                   'forty-first', 'forty-second', 'forty-third', 'forty-fourth', 'forty-fifth', 'forty-sixth', 'forty-seventh', 'forty-eighth', 'forty-ninth', 'fiftieth',
                   'fifty-first', 'fifty-second', 'fifty-third', 'fifty-fourth', 'fifty-fifth', 'fifty-sixth', 'fifty-seventh', 'fifty-eighth', 'fifty-ninth', 'sixtieth',
                   'sixty-first', 'sixty-second', 'sixty-third', 'sixty-fourth', 'sixty-fifth', 'sixty-sixth', 'sixty-seventh', 'sixty-eighth', 'sixty-ninth', 'seventieth',
                   'seventy-first', 'seventy-second', 'seventy-third', 'seventy-fourth', 'seventy-fifth', 'seventy-sixth', 'seventy-seventh', 'seventy-eighth', 'seventy-ninth', 'eightieth',
                   'eighty-first', 'eighty-second', 'eighty-third', 'eighty-fourth', 'eighty-fifth', 'eighty-sixth', 'eighty-seventh', 'eighty-eighth', 'eighty-ninth', 'ninetieth',
                   'ninety-first', 'ninety-second', 'ninety-third', 'ninety-fourth', 'ninety-fifth', 'ninety-sixth', 'ninety-seventh', 'ninety-eighth', 'ninety-ninth', 'one hundredth']

months = ['january', 'february', 'march', 'april', 'may', 'june', 'july',
          'august', 'september', 'october', 'november', 'december']

roman_num = ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x', 'xi', 'xii', 'xiii', 'xiv', 'xv', 'xvi', 'xvii', 'xviii', 'xix', 'xx', 'xxi', 'xxii', 'xxiii', 'xxiv', 'xxv', 'xxvi', 'xxvii', 'xxviii', 'xxix', 'xxx', 'xxxi', 'xxxii', 'xxxiii', 'xxxiv', 'xxxv', 'xxxvi', 'xxxvii', 'xxxviii', 'xxxix', 'xl', 'xli', 'xlii', 'xliii', 'xliv', 'xlv', 'xlvi', 'xlvii', 'xlviii', 'xlix', 'l', 'li', 'lii', 'liii', 'liv', 'lv', 'lvi', 'lvii', 'lviii', 'lix', 'lx', 'lxi', 'lxii', 'lxiii', 'lxiv', 'lxv', 'lxvi', 'lxvii', 'lxviii', 'lxix', 'lxx', 'lxxi', 'lxxii', 'lxxiii', 'lxxiv', 'lxxv', 'lxxvi', 'lxxvii', 'lxxviii', 'lxxix', 'lxxx', 'lxxxi', 'lxxxii', 'lxxxiii', 'lxxxiv', 'lxxxv', 'lxxxvi', 'lxxxvii', 'lxxxviii', 'lxxxix', 'xc', 'xci', 'xcii', 'xciii', 'xciv', 'xcv', 'xcvi', 'xcvii', 'xcviii', 'xcix']

prepositions = [
    'about', 'above', 'across', 'after', 'against', 'along', 'among', 'around',
    'as', 'at', 'before', 'behind', 'below', 'beneath', 'beside', 'between',
    'beyond', 'by', 'concerning', 'considering', 'despite', 'down', 'during',
    'except', 'for', 'from', 'in', 'inside', 'into', 'like', 'near', 'of',
    'off', 'on', 'onto', 'out', 'outside', 'over', 'past', 'regarding',
    'round', 'since', 'through', 'throughout', 'to', 'toward', 'under',
    'underneath', 'until', 'unto', 'up', 'upon', 'with', 'within', 'without'
]


# words removed individually
useless_words = months + ['and', 'on', 'volume', 'the', 'and', 'from', 'for', 'xa', 'xx', 'uu', 'th', 'eaap', 'of', 'ca', 'app', 'ww', 'with', 'ba', 'ss', 'nd', 'rd', 'st'] + roman_num + prepositions


# substrings removed directly.
bad_strings = numeric_strings + ['xa', '聽鈥', '茅', '眉'] + ['‚', '・', '\ue161', '︽', '•', '\ue0d3', '㈣', '−', '¡', '£', '³', '‒', '〃', '”', '€', '<', '»', '\ue131', '>', '′', '＄', '·', '‐', '\ue76c', '\ue0a2', '—', '¹', '+', '∈', '┒', '\ue7fc', '`', '\ue011', '|', '\ue756', '▼', '\ue046', '@', '¬', '\ue11f', '﹁', '%', '\ue21c', '\ue1bc', '¯', '︿', '▓', '\ue15d', '¾', '\ue15e', '¼', '︾', '#', '╁', '*', '^', '\ue21a', '~', '«', '\ue047', '‘', '©', '\ue044', '℃', '„', '\u200b', '⁃', '\ue0c7', '\ue219', '®', '\ue15c']

def to_json(obj, name='check.json'):
    try:
        with open(name, 'w') as f:
            json.dump(obj, f, indent=4)
    except TypeError:
        with open(name, 'w') as f:
            json.dump(str(obj), f, indent=4)

def column_to_list(df_col: pd.Series):
    temp = df_col.dropna().drop_duplicates().to_list()
    temp.sort(key=len)
    return temp

def column_to_json(df_col: pd.Series, name='check.json'):
    to_json(column_to_list(df_col), name)

def filter_string(input_string, all_must_include=[], any_include=[], none_must_include=[], any_exclude=[]):
    # 判断全部元素都需要是子串的情况
    for substring in all_must_include:
        if substring not in input_string:
            return False

    # 判断只要有一个是子串的情况
    if any_include:
        for substring in any_include:
            if substring in input_string:
                break
        else:
            return False

    # 判断全部元素都不是子串的情况
    for substring in none_must_include:
        if substring in input_string:
            return False

    # 判断只要有一个元素不是子串的情况
    if any_exclude:
        for substring in any_exclude:
            if substring not in input_string:
                break
        else:
            return False

    return True

def count_and_sort_word_frequency(text):
    """
    统计文本中每个单词的词频，并按词频从大到小排序

    参数：
    text (str): 输入的文本

    返回值：
    list: 按词频从大到小排序的单词列表和对应的词频列表，每个元素为元组 (word, frequency)
    """
    # 将文本转换为小写，方便词频统计时忽略大小写
    lower_text = text.lower()

    # 使用正则表达式分割文本为单词列表
    import re
    word_list = re.findall(r'\b\w+\b', lower_text)

    # 统计词频
    word_frequency = {}
    for word in word_list:
        word_frequency[word] = word_frequency.get(word, 0) + 1

    # 按词频从大到小排序
    sorted_word_frequency = sorted(word_frequency.items(), key=lambda x: x[1], reverse=True)

    return sorted_word_frequency
