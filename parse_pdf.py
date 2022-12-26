# importing libraries

import spacy
import re
import nltk

from spacy.matcher import Matcher
from tika import parser


def get_text(file):
    file_data = parser.from_file(file)
    return file_data['content']


def resume_parser(file):
    text = get_text(file)
    parsed_content = {}

    email = get_email_addresses(text)
    parsed_content['e-mail'] = email

    phone_number = get_phone_numbers(text)
    if len(phone_number) <= 10:
        parsed_content['phone number'] = phone_number

    name = extract_name(text)
    parsed_content['name'] = name

    # Keywords that we want to extract
    keywords = ["education",
                "summary",
                "accomplishments",
                "work background",
                "other activities",
                "qualifications",
                "experience",
                "interests",
                "skills",
                "achievements",
                "certifications",
                "projects",
                "internships",
                "trainings",
                "hobbies",
                "jobs"
                ]
    # Cleaning unwanted text
    text = text.replace("\n", " ")
    text = text.replace("[^a-zA-Z0-9]", " ")
    re.sub('\W+', '', text)
    text = text.lower()

    content = {}
    indices = []
    keys = []
    for key in keywords:
        try:
            content[key] = text[text.index(key) + len(key):]
            indices.append(text.index(key))
            keys.append(key)

        except:
            pass

    # Sorting the indices
    zipped_lists = zip(indices, keys)
    sorted_pairs = sorted(zipped_lists)

    tuples = zip(*sorted_pairs)
    indices, keys = [list(tup) for tup in tuples]

    # Keeping the required content and removing the redundant part
    content = []
    for idx in range(len(indices)):
        if idx != len(indices) - 1:
            content.append(text[indices[idx]: indices[idx + 1]])
        else:
            content.append(text[indices[idx]:])

    for i in range(len(indices)):
        parsed_content[keys[i]] = content[i]

    # return the parsed content
    return parsed_content


# E-mail extraction
def get_email_addresses(string):
    r = re.compile(r'[\w\.-]+@[\w\.-]+')
    print(r.findall(string))
    emails_found = r.findall(string)
    return emails_found


# phone-number extraction
def get_phone_numbers(string):
    r = re.compile(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
    phone_numbers = r.findall(string)
    print(phone_numbers)
    phn_numbers_found = [re.sub(r'\D', '', num) for num in phone_numbers]
    return phn_numbers_found


# Name extraction
nlp = spacy.load('en_core_web_sm')
matcher = Matcher(nlp.vocab)


def extract_name(text):
    nlp_text = nlp(text)

    # First name and Last name are always Proper Nouns
    pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]

    matcher.add('name', [pattern], on_match=None)

    matches = matcher(nlp_text)

    for match_id, start, end in matches:
        span = nlp_text[start:end]
        return span.text

def skills_exract(string):
    skills

