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
import random


TRANSLATE_PROBABILITY = 0.5
PUNCTUATION = '",.:;()#!$%&*+-/<=>?@[]_~'

# read API key from local txt file
with open('key.txt', 'r') as f:
    key = f.readline()


# use webster API to retrieve a list of synonyms for the specified word
def get_syns(word):
    url = 'https://dictionaryapi.com/api/v3/references/thesaurus/json/' + word

    key_data = {'key': key}
    request = requests.get(url, params=key_data)

    # if the API can't find any synonyms, return 0
    try:
        return request.json()[0]['meta']['syns']

    except:
        return -1


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
def get_syn_index(length):
    return random.randrange(0, length)


def should_translate():
    r = random.random()
    return r < TRANSLATE_PROBABILITY


# replace every word in the input file (except for those in no_change)
# with that word's synonym and put it in the output file
def main():
    syns = load_thesaurus()
    no_change = load_no_change()

    with open('input.txt', 'r') as fin, open('output.txt', 'w') as fout:
        for line in fin:
            for word in line.split():

                if not should_translate:
                    fout.write(word + ' ')
                    continue

                # remove punctuation from word to prevent duplicate dictionary entries
                stripped_word = word.translate(
                    str.maketrans('', '', PUNCTUATION))

                # if the word shouldn't be changed, add it directly to the output
                if stripped_word in no_change:
                    fout.write(word + ' ')
                    continue

                # if the word isn't already in the dictionary, make an API request
                # to put it in. If the request fails, add the word directly to output
                if stripped_word not in syns:
                    result = get_syns(stripped_word)
                    if result == -1:
                        no_change.append(stripped_word)
                        fout.write(word + ' ')
                        continue

                    syns[stripped_word] = result

                # get a synonym from the list
                syn_list = syns[stripped_word][0]
                i = get_syn_index(len(syn_list))
                synonym = syn_list[i]

                # put a period in if the original word had it
                if word[-1] == '.':
                    synonym += '.'

                fout.write(synonym + ' ')

            fout.write('\n')

    # save synonym and no_change to their JSON files
    with open('thesaurus.json', 'w') as f:
        json.dump(syns, f)

    with open('no_change.json', 'w') as f:
        json.dump(no_change, f)


main()
