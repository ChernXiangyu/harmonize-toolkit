import pandas as pd
from rapidfuzz import fuzz, process
import random
from tqdm import tqdm
import re
import unicodedata
from harmonize_toolkit.preprocess import *
from itertools import filterfalse

def lowercase_processor(s):
    return s.lower()

def getStringIntersectionList(stringList: list):
    stringNum = len(stringList)
    if stringNum == 0:
        return []
    if stringNum == 1:
        return stringList[0].split()
    lists = [string.split() for string in stringList]
    # 将第一个列表转换为集合
    intersection_set = set(lists[0])

    # 计算交集
    for lst in lists[1:]:
        intersection_set = intersection_set.intersection(lst)

    # 保持原始列表中的顺序
    intersection_list = [x for x in lists[0] if x in intersection_set]
    return intersection_list

def getKeyword(strings: list, scorer=fuzz.token_sort_ratio, score_cutoff=90, process_function=preprocessString):
    processed_strings = [process_function(string) for string in strings]
    processed_strings = remove_duplicates(processed_strings)
    processed_strings.sort(key=len, reverse=True)
    # 保证计算速度均衡
    keywords = []
    old_len = len(processed_strings)
    checked = set()

    with tqdm(total=old_len) as pbar:
        for sample in processed_strings:
            if sample not in checked:
                extract_res = process.extract(sample, processed_strings, scorer=scorer, score_cutoff=score_cutoff)
                similar_strings = [entity[0] for entity in extract_res]
                for string in similar_strings:
                    if string not in checked:
                        checked.add(string)
                        pbar.update(1)
                word_list = getStringIntersectionList(similar_strings)
                if word_list:
                    keyword = ' '.join(word_list)
                    keywords.append(keyword)
    keywords = remove_duplicates(keywords)
    return keywords
        

def is_subsequence(keywordList, targetString):
    '''Checks if the words in the string list appear in order in the target string'''
    keyword = ' '.join(keywordList)
    intersection_list = getStringIntersectionList([keyword, targetString])
    if len(intersection_list) == len(keywordList):
        return True
    else:
        return False

def matchKeyword(keywords: list, strings: list, process_function=preprocessString, scorer=fuzz.token_sort_ratio):
    keywords = remove_duplicates(keywords)
    strings = remove_duplicates(strings)
    keywords.sort(key=len, reverse=True)
    match_res = {}
    for keyword in keywords:
        match_res[keyword] = []
    matched = set()
    old_len = len(strings)
    with tqdm(total=old_len) as pbar:
        for keyword in keywords:
            for string in strings:
                if is_subsequence(keyword.split(), process_function(string)) and string not in matched:
                    match_res[keyword].append(string)
                    matched.add(string)
                    pbar.update(1)

        if len(matched) != len(strings):
            for string in strings:
                if string not in matched:
                    most_similar = process.extractOne(process_function(string), keywords, scorer=scorer)[0]
                    match_res[most_similar].append(string)
                    strings.remove(string)
                    pbar.update(1)

    return match_res


def fuzzMatchKeyword(keywords: list, strings: list, process_function=preprocessString, scorer=fuzz.token_sort_ratio):
    keywords.sort(key=len, reverse=True)
    match_res = {keyword: [] for keyword in keywords}
    old_len = len(strings)
    new_sample = []
    with tqdm(total=old_len) as pbar:
        for string in strings:
            most_similar = process.extractOne(process_function(string), keywords, scorer=scorer)[0]
            match_res[most_similar].append(string)
            pbar.update(1)
        new_sample.append(string)

    return match_res

def group_strings_by_similarity(word_list: list, score_cutoff=90, scorer=fuzz.token_sort_ratio, process_function=preprocessString):
    group_res = []
    checked = set()
    processed_word_list = [w for w in word_list]
    processed_word_list = remove_duplicates(processed_word_list)
    for word in tqdm(processed_word_list):
        if word not in checked:
            extract_res = process.extract(word, processed_word_list, score_cutoff=score_cutoff, scorer=scorer, processor=process_function)
            similar_strings = [res[0] for res in extract_res if res[0] not in checked]
            group_res.append(similar_strings)
            checked.update(similar_strings)
    return group_res

def extract_dict_by_keys(input_dict, keys_to_extract):
    return {k: input_dict[k] for k in keys_to_extract if k in input_dict}

def fuzz_filter_string(input_string, all_must_include=[], any_include=[], none_must_include=[], any_exclude=[], score_cutoff=90):
    # 判断全部元素都需要是子串的情况
    for substring in all_must_include:
        # if substring not in input_string:
        if fuzz.partial_ratio(substring, input_string) < 100 - score_cutoff:
            return False

    # 判断只要有一个是子串的情况
    if any_include:
        for substring in any_include:
            # if substring in input_string:
            if fuzz.partial_ratio(substring, input_string) > score_cutoff:
                break
        else:
            return False

    # 判断全部元素都不是子串的情况
    for substring in none_must_include:
        # if substring in input_string:
        if fuzz.partial_ratio(substring, input_string) > score_cutoff:
            return False

    # 判断只要有一个元素不是子串的情况
    if any_exclude:
        for substring in any_exclude:
            if fuzz.partial_ratio(substring, input_string) < 100 - score_cutoff:
            # if substring not in input_string:
                break
        else:
            return False

    return True