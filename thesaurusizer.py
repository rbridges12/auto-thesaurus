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
import os
import string


# read API key from local txt file
with open('key.txt', 'r') as f:
    key = f.readline()


# use webster API to retrieve a list of synonyms for the specified word
def get_syns(word):
    url = 'https://dictionaryapi.com/api/v3/references/thesaurus/json/' + word

    key_data = {'key': key}
    request = requests.get(url, params=key_data)

    return request.json()[0]['meta']['syns']


# load the thesaurus dictionary from JSON file
# if it's empty, return an empty dict
def load_thesaurus():
    if os.stat('thesaurus.json').st_size == 0:
        return {}

    with open('thesaurus.json', 'r') as f:
        return json.load(f)


# load words that shouldn't be changed from JSON
def load_no_change():
    if os.stat('no_change.json').st_size == 0:
        return {}

    with open('no_change.json', 'r') as f:
        return json.load(f)


# return the index corresponding to the synonym to be chosen
# TODO: make random
def get_syn_index():
    return 0


# replace every word in the input file (except for those in no_change)
# with that word's synonym and put it in the output file
def main():
    syns = load_thesaurus()
    no_change = load_no_change()

    with open('input.txt', 'r') as fin, open('output.txt', 'w') as fout:
        for line in fin:
            for word in line.split():

                # remove punctuation from word to prevent duplicate dictionary entries
                stripped_word = word.translate(
                    None, '",.:;()#!$%&*+-/<=>?@[]_~')

                # if the word shouldn't be changed, add it directly to the output
                if stripped_word in no_change:
                    fout.write(word + ' ')

                else:
                    # if the word isn't already in the dictionary, make an API request
                    # to put it in
                    if stripped_word not in syns:
                        syns[stripped_word] = get_syns(stripped_word)

                    # get a synonym from the list
                    synonym = syns[stripped_word][0][get_syn_index()]

                    # put a period in if the original word had it
                    if word[-1] == '.':
                        synonym += '.'

                    fout.write(synonym + ' ')

            fout.write('\n')

    with open('thesaurus.json', 'w') as f:
        json.dump(syns, f)


main()
