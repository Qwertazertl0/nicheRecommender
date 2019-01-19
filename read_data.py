from yelpapi import YelpAPI
import json

def read_data():
    with open(filename, encoding="utf8") as f:
        for line in f:
            j = json.loads(line)
            print(j)
