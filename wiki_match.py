import os
import json
import wikipedia
import langid
from tqdm import tqdm
import time
from harmonize_toolkit.nlp import *

def wiki_search_match(ents, name, translation=False):
    search_res_file = f'{name}_search_res.json'
    mem_file = f'{name}_mem.json'
    
    if not os.path.isfile(search_res_file):
        with open(search_res_file, 'w') as f:
            json.dump({}, f, indent=4)
    
    if not os.path.isfile(mem_file):
        with open(mem_file, 'w') as f:
            json.dump(0, f, indent=4)
    
    with open(search_res_file, 'r') as f:
        search_res = json.load(f)
    
    with open(mem_file, 'r') as f:
        mem = json.load(f)
    
    for i in tqdm(range(mem, len(ents))):
        # print(len(ents))
        if translation:
            language = langid.classify(ents[i])[0]
        else:
            language = 'en'
        wikipedia.set_lang(language)
        temp_search_res = wikipedia.search(ents[i], suggestion=True)
        if temp_search_res:
            res = temp_search_res[0]
        else:
            res = [temp_search_res[1]]
        temp_res = {ents[i]: res}
        search_res.update(temp_res)
        
        with open(search_res_file, 'w') as f:
            json.dump(search_res, f, indent=4)
        
        with open(mem_file, 'w') as f:
            json.dump(mem, f, indent=4)
        # time.sleep(1)
        mem = i

def replace_bad_dict_value(dictionary: dict):
    replaced_dict = {}
    for key, value in dictionary.items():
        if len(value) < 2:
            replaced_dict[key] = [key]
        else:
            replaced_dict[key] = value
    return replaced_dict

def remove_person_in_value(dictionary: dict):
    filted_dict = {}
    for key, value in tqdm(dictionary.items()):
        filted_value = list(filter(lambda x: not is_person(x), value))
        # print(filted_value)
        filted_dict[key] = filted_value
    return filted_dict

def remove_person_key(dictionary: dict):
    filted_dict = {}
    for key in tqdm(dictionary):
        if not is_person(key):
            filted_dict[key] = dictionary[key]
    return filted_dict

def merge_match_result(match_result: dict, name_map: dict):
    for key, value in name_map.items():
        if value in match_result and key in match_result:
            match_result[value].extend(match_result[key])
            match_result.pop(key)
        elif key in match_result and value not in match_result:
            match_result[value] = match_result[key]
            match_result.pop(key)
        
    return match_result