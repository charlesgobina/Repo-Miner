'''
This file contains utility functions that are used in the main script
'''
import json
import requests


class NoInternetConnectionError(Exception):
    """Custom exception for no internet connection."""
    pass

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


def check_internet_connection():
    '''
    Check for an internet connection
    '''
    try:
        # Trying to access a website (e.g., Google) to check for an internet
        # connection
        response = requests.get('http://www.google.com', timeout=5)
        response.raise_for_status()  # This will raise an HTTPError for bad responses
        return True
    except requests.ConnectionError:
        return False
    except requests.Timeout:
        return False
    except requests.RequestException:
        return False
