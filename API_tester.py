import requests

#  read API key from local txt file
with open('key.txt', 'r') as f:
    key = f.readline()

word = 'dont'
url = 'https://dictionaryapi.com/api/v3/references/thesaurus/json/' + word

key_data = {'key': key}
request = requests.get(url, params=key_data)

with open('API_test.json', 'w') as f:
    f.write(request.text)
