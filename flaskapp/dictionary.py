#brings straight to the website and has a search bar on chrome
class Word:
    def __init__ (self, word, origin, subWords):
        self.word = word
        self.origin = origin
        self.subWords = subWords
        self.pronunciation = self.subWords[0].pronunciation
    
    def compile_json(self):
        for each in self.subWords:
            each.clean_examples()
        
        data = {}
        data["word"] = self.word
        data["phonetic"] = self.pronunciation
        data["origin"] = self.origin
        data["meaning"] = {}

        for sword in self.subWords:
            current = []
            for z in range(len(sword.definitions)):
                temp = {}
                temp["definition"] = sword.definitions[z]
                temp["example"] = sword.examples[z]

                current.append(temp)
            data["meaning"][sword.partOfSpeech] = current
        return data

    
class SubWord:
    def __init__(self, partOfSpeech, definitions, examples, pronunciation):
        self.partOfSpeech = partOfSpeech
        self.definitions = definitions
        self.examples = examples
        self.pronunciation = pronunciation

    def clean_examples(self):
        new_examples = []
        for each in self.examples:
            temp = []
            for each2 in each:
                if (each2 != None):
                    temp.append(each2["text"])
                else:
                    temp.append(None)
            new_examples.append(temp)
        self.examples = new_examples