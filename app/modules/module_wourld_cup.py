import json

def getFlags(country):
    with open('data/flags.json', 'r') as f:
        flags = json.load(f)
        return flags[country]
