import json

def read_json_files(file_name):
    with open(file_name,'r') as f:
        return json.load(f)