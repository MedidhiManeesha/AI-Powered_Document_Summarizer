import re
import builtins
import keyword
from collections import defaultdict

def my_reduce(func, sequence, initial_value=None):
    iterable = iter(sequence)
    if initial_value is None:
        value = next(iterable)
    else:
        value = initial_value
    for elem in iterable:
        value = func(value, elem)
    return value

def strip_special_chars(docx):
    new_string = re.sub(r"\W+", " ", docx)
    return new_string

def get_reserved_word_frequency(docx):
    cleaned_docx = strip_special_chars(docx)
    reserved_keyword_dict = defaultdict(int)
    identifier_dict = defaultdict(int)
    builtins_dict = defaultdict(int)
    for i in cleaned_docx.split():
        if i in keyword.kwlist:
            reserved_keyword_dict[i] += 1
        elif i in list(dir(builtins)):
            builtins_dict[i] += 1
        else:
            identifier_dict[i] += 1
    results = {
        "reserved": reserved_keyword_dict,
        "identifiers": identifier_dict,
        "builtins": builtins_dict
    }
    return results
