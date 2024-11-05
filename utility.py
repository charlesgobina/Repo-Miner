'''
This file contains utility functions that are used in the main script
'''
import json

# function to open json file

def open_json_file(json_file):
    '''
    Open a json file and return the data
    '''
    with open(json_file, "r", encoding='utf-8') as f:
        data1 = json.load(f)
    return data1

# function to write json file

def write_json_file(json_file, data):
    '''
    Write data to a json file
    '''
    with open(json_file, "w", encoding='utf-8') as f:
        json.dump(data, f, indent=4)
    return
