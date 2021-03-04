# test webster API

# format api response into a list of synonyms

# make a JSON file to save a personal copy of the data taken from the API
# so duplicate API requests can be avoided
# maybe sort it for faster lookups?

# iterate through every word in the input file, put it's synonym in the output file

# add options for synonyms to be chosen sequentially or randomly,
# how many words to replace, etc

import requests
import json

word = 'mesmerized'
url = 'https://dictionaryapi.com/api/v3/references/thesaurus/json/' + word

# read key from local txt file
with open('key.txt', 'r') as f:
    key = f.readline()

# send request
key_data = {'key': key}
request = requests.get(url, params=key_data)

word_syns = request.json()[0]['meta']['syns']



