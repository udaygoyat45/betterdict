def information(word):
    import urllib.request, json
    base_url = r"https://googledictionaryapi.eu-gb.mybluemix.net/?define="
    json_url = urllib.request.urlopen((base_url+word))
    data = json.loads(json_url.read())[0]
    return data
