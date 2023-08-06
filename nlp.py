import pandas as pd
import spacy
from spacy import displacy
from tqdm import tqdm
import sys

import openai

openai.api_key = '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'

def is_person_gpt(string: str):
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
            {"role": "system", "content": "You will receive a string, and you need to determine whether this string is a person's name or not. You can only answer 'yes' or 'no'."},
            {"role": "user", "content": "Ada Lovelace Fellowship"},
            {"role": "assistant", "content": "no"},
            {"role": "user", "content": string}
        ]
    )
    response_string = response['choices'][0]['message']['content']
    if 'yes' in response_string.lower():
        return True
    return False

def extract_organizations_gpt(string: str):
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    temperature = 0.1,
    messages=[
            {"role": "system", "content": "You will receive a string, and you need to extract all the organizations in this string. The form you reply should be a python list. If the input seems to be incomplete or incorrect, reply an empty python list."},
            {"role": "user", "content": "University of California - Santa Cruz\nAllison Druin, University of Maryland - College Park\nAlan Borning, University of Washington\nEdward Lank, University of Waterloo"},
            {"role": "assistant", "content": "['University of California - Santa Cruz', 'University of Maryland - College Park', ' University of Washington']"},
            
            {"role": "user", "content": "penn state university, laboratory for perception, action, and cognition (lpac)"},
            {"role": "assistant", "content": "['penn state university']"},
            
            
            {"role": "user", "content": string}
        ]
    )
    response_string = response['choices'][0]['message']['content']

    return response_string 

def extract_schools_gpt(string: str):
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    temperature = 0.1,
    messages=[
            {"role": "system", "content": "You will receive a string, and you need to extract all the schools in this string. The form you reply should be a python list. If the input seems to be incomplete or incorrect, reply an empty python list."},
            {"role": "user", "content": "University of California - Santa Cruz\nAllison Druin, University of Maryland - College Park\nAlan Borning, University of Washington\nEdward Lank, University of Waterloo"},
            {"role": "assistant", "content": "['University of California - Santa Cruz', 'University of Maryland - College Park', ' University of Washington']"},
            
            {"role": "user", "content": 'Northwestern University, Sivaraman Balakrishnan, Carnegie Mellon University'},
            {"role": "assistant", "content": "['Northwestern University', 'Carnegie Mellon University']"},

            {"role": "user", "content": 'University of Granada (Spain) + ENSTA, Institut Polytechnique Paris, Inria. Lorenzo Baraldi, University of Modena and Reggio Emilia'},
            {"role": "assistant", "content": "['University of Granada (Spain)', 'Institut Polytechnique Paris', 'University of Modena and Reggio Emilia']"},
            
            {"role": "user", "content": string}
        ]
    )
    response_string = response['choices'][0]['message']['content']

    return response_string 

def get_abbreviation_gpt(string: str):
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    temperature = 0.1,
    messages=[
            {"role": "system", "content": "You will receive a string representing a school, and you need to put all the aliases and abbreviations of this school into a Python list. Then send it to me."},
            {"role": "user", "content": "University of California, Berkeley"},
            {"role": "assistant", "content": "['University of California at Berkeley', 'UCB', 'UC Berkeley', 'University of California, Berkeley']"},
            
            {"role": "user", "content": "CUNY"},
            {"role": "assistant", "content": "['CUNY', 'The City University of New York']"},
            
            
            {"role": "user", "content": string}
        ]
    )
    response_string = response['choices'][0]['message']['content']

    return response_string 

nlp = spacy.load("en_core_web_lg")

def get_school_name_list_gpt(string: str):
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    temperature = 0.1,
    messages=[
            {"role": "system", "content": "You are given a string that represents a school. You need to extract the name of the school from the string, excluding the college, department or faculty name. Reply to me with a Python list containing the school name, any alternative names for the school, and any abbreviations for the school. If you couldn't find any alternative names or abbreviations for this specific school, reply an empty python list."},
            {"role": "user", "content": "The George Washington University School of Medicine and Health Sciences"},
            {"role": "assistant", "content": "['The George Washington University', 'GWU', 'GW']"},
            
            {"role": "user", "content": "University of Michigan College of Literature, Science, and the Arts"},
            {"role": "assistant", "content": "['University of Michigan', 'UMich']"},
            
            {"role": "user", "content": 'University “Ss. Cyril and Methodius” Faculty of Electrical Engineering and Information Technologies'},
            {"role": "assistant", "content": "['Ss. Cyril and Methodius University of Skopje', 'UKIM']"},

            {"role": "user", "content": 'State University of New York College of Environmental Science and Forestry'},
            {"role": "assistant", "content": "['State University of New York', 'SUNY']"},

            {"role": "user", "content": 'No.2 Secondary School Attached to East China Normal University'},
            {"role": "assistant", "content": "['No.2 Secondary School Attached to East China Normal University', 'HSEFZ']"},

            {"role": "user", "content": string}
        ]
    )
    response_string = response['choices'][0]['message']['content']

    return response_string 

old_dict1 = {"ENSEEIHT - Ecole Nationale Supérieure d'Electrotechnique, d'Electronique, d'Informatique, d'Hydraulique et des Télécommunications": ["ENSEEIHT - Ecole Nationale Supérieure d'Electrotechnique, d'Electronique, d'Informatique, d'Hydraulique et des Télécommunications", "Ecole Nationale Supérieure d'Electrotechnique, d'Electronique, d'Informatique, d'Hydraulique et des Télécommunications", 'ENSEEIHT']}

school_alias_dict1 = {
    "ENSEEIHT - Ecole Nationale Supérieure d'Electrotechnique, d'Electronique, d'Informatique, d'Hydraulique et des Télécommunications": [
        "ENSEEIHT - Ecole Nationale Supérieure d'Electrotechnique, d'Electronique, d'Informatique, d'Hydraulique et des Télécommunications",
        "Ecole Nationale Supérieure d'Electrotechnique, d'Electronique, d'Informatique, d'Hydraulique et des Télécommunications",
        'ENSEEIHT',
        'N7'
    ]
}

old_dict2 =  {'National Research Nuclear University MEPhI (Moscow Engineering Physics Institute)': ['National Research Nuclear University MEPhI (Moscow Engineering Physics Institute)', 'National Research Nuclear University MEPhI', 'Moscow Engineering Physics Institute', 'NRNU MEPhI']}

school_alias_dict2 = {
    'National Research Nuclear University MEPhI (Moscow Engineering Physics Institute)': [
        'National Research Nuclear University MEPhI (Moscow Engineering Physics Institute)',
        'National Research Nuclear University MEPhI',
        'Moscow Engineering Physics Institute',
        'NRNU MEPhI',
        'MEPhI'
    ]
}


def correct_school_name_list_gpt(string: str):
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    temperature = 0.0,
    messages=[
        
            {"role": "system", "content": "You will receive a Python dictionary consisting of a school's full name and its aliases, with the full name as the key and the aliases stored in a list. Please respond with a Python dictionary in the same format, supplementing other aliases and correcting incorrect aliases. You MUST reply a Python dictionary!"},
            
            {"role": "user", "content": f"{old_dict1}"},
            {"role": "assistant", "content": f"{school_alias_dict1}"},
            
            {"role": "user", "content": f"{old_dict2}"},
            {"role": "assistant", "content": f"{school_alias_dict2}"},


            {"role": "user", "content": string}
        ]
    )
    response_string = response['choices'][0]['message']['content']

    return response_string 

def get_official_name_gpt(string: str):
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    temperature = 0.0,
    messages=[
        
            {"role": "system", "content": '''   Because the names of institutions may vary for different databases, your current task is to unify the different names corresponding to the same institution into the most official name. You will now receive a string representing an organization. Please identify the name of the institution based on this string and reply with the most official and formal name of the institution.

                                                For universities, there may also be mentions of colleges. Please do not include the name of the college in your reply, only include the most official and formal name of the university.

                                                Some institution names may be abbreviations. Please reply with the institution's most official full English name.

                                                If you couldn't find any information about the institution, just reply an empty string.

                                                You only need to reply with a Python string.'''},
            
            {"role": "user", "content": f"University of California, Irvine - College of Medicine"},
            {"role": "assistant", "content": f"University of California, Irvine"},

            {"role": "user", "content": string}
        ]
    )
    response_string = response['choices'][0]['message']['content']

    return response_string 

def extract_university_name_gpt(string: str):
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    temperature = 0.0,
    messages=[
        
            {"role": "system", "content": '''  '''},
            
            {"role": "user", "content": f"University of California, Irvine - College of Medicine"},
            {"role": "assistant", "content": f"University of California, Irvine"},

            {"role": "user", "content": string}
        ]
    )
    response_string = response['choices'][0]['message']['content']

    return response_string 

nlp = spacy.load("en_core_web_lg")

def visualize_entities(string: str):
    doc = nlp(string)
    displacy.render(doc, style='ent', jupyter=True)

def is_meaningless_string(text):
    doc = nlp(text)
    entities = doc.ents

    if entities:
        return False
    
    return True

def extract_organizations(string: str):
    """
    Extracts organizations from the given string.
    
    Args:
        string (str): The input string to extract organizations from.
    
    Returns:
        list: A list of organizations extracted from the input string.
    """
    res = []
    doc = nlp(string)
    for ent in doc.ents:
        if ent.label_ == 'ORG':
            res.append(ent.text)
    return res

def extract_persons(string: str):
    """
    Extracts persons (names) from the given string.
    
    Args:
        string (str): The input string to extract persons from.
    
    Returns:
        list: A list of persons (names) extracted from the input string.
    """
    res = []
    doc = nlp(string)
    for ent in doc.ents:
        if ent.label_ == 'PERSON':
            res.append(ent.text)
    return res

def extract_gpes(string: str):
    """
    Extracts GPEs (Geopolitical Entities) from the given string.
    
    Args:
        string (str): The input string to extract GPEs from.
    
    Returns:
        list: A list of GPEs extracted from the input string.
    """
    res = []
    doc = nlp(string)
    for ent in doc.ents:
        if ent.label_ == 'GPE':
            res.append(ent.text)
    return res

def analyze_entity(entity: str):
    """
    Analyzes the entities (persons, organizations, and GPEs) from the given string.
    
    Args:
        entity (str): The string to analyze entities from.
    
    Returns:
        dict: A dictionary containing the entity, persons, organizations, and GPEs extracted from the input string.
    """
    # persons = extract_persons(entity)
    # organizations = extract_organizations(entity)
    # gpes = extract_gpes(entity)

    persons = []
    organizations = []
    gpes = []

    doc = nlp(entity)
    for ent in doc.ents:
        if ent.label_ == 'GPE':
            gpes.append(ent.text)
        elif ent.label_ == 'PERSON':
            gpes.append(ent.text)
        elif ent.label_ == 'ORG':
            organizations.append(ent.text)
            
    return {'entity': entity, 'persons': persons, 'organizations': organizations, 'gpes': gpes}


def analyze_entities(entities: list):
    """
    Analyzes entities (persons, organizations, and GPEs) from the given list of strings.
    
    Args:
        entities (list): A list of strings to analyze entities from.
    
    Returns:
        list: A list of dictionaries, each containing the entity, persons, organizations, and GPEs extracted from the input list.
    """
    res = []

    for entity in tqdm(entities):
        res.append(analyze_entity(entity))
        
    return res

def is_person(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.text == text and ent.label_ == "PERSON":
            return True
    return False

def is_gpe(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.text == text and ent.label_ == "GPE":
            return True
    return False

def is_org(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.text == text and ent.label_ == "ORG":
            return True
    return False