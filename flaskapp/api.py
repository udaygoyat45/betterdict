# old classic:
'''
def information(word):
    import urllib.request, json
    base_url = r"https://googledictionaryapi.eu-gb.mybluemix.net/?define="
    json_url = urllib.request.urlopen((base_url+word))
    data = json.loads(json_url.read())[0]
    return data
'''

from flaskapp.dictionary import Word, SubWord
import requests
import json


def information(word):
    app_id = "9980cb73"
    app_key = "06d577adc31a2f72d9f75fcee6f6c77b"
    language = "en-gb"
    word_id = word
    url = "https://od-api.oxforddictionaries.com:443/api/v2/entries/" + \
        language + "/" + word_id.lower()
    r = requests.get(url, headers={"app_id": app_id, "app_key": app_key})
    return r.json()


def extract(word_id):
    # getting data:
    data = information(word_id)

    # declarations:
    subwords = []
    origin = ""

    # processing:
    main = data["results"][0]["lexicalEntries"]

    for each in main:
        part_of_speech = each["lexicalCategory"]["id"]
        pronunciation = each["pronunciations"][0]["phoneticSpelling"]
        if ("etymologies" in each["entries"][0].keys()):
            origin = each["entries"][0]["etymologies"][0]

        definitions = []
        examples = []
        for definition in each["entries"][0]["senses"]:
            definitions.append(definition["definitions"][0])
            try:
                examples.append(definition["examples"])
            except:
                examples.append([None])

        subwords.append(
            SubWord(part_of_speech, definitions, examples, pronunciation))
    return Word(word_id, origin, subwords)
