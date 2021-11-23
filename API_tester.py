import requests

#  read API key from local txt file
with open('key.txt', 'r') as f:
    key = f.readline()

word = 'motivation'
url = 'https://dictionaryapi.com/api/v3/references/thesaurus/json/' + word
url_datamuse = 'https://api.datamuse.com/words?ml=' + word

# key_data = {'key': key}
# request = requests.get(url, params=key_data)

request = requests.get(url_datamuse)

with open('API_test.json', 'w') as f:
    f.write(request.text)
