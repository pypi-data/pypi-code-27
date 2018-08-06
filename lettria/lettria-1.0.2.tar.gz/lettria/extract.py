class Extract:
    def __init__(self, key=None):
        None
    def NLP(json):
        if json and 'NLP' in json:
            return json['NLP']
        else:
            return None
    def NER(json):
        if json and 'NER' in json:
            return json['NER']
        else:
            return None
    def NLU(json):
        if json and 'NLU' in json:
            return json['NLU']
        else:
            return None
    def Sentiment(json):
        if json and 'Sentiment' in json:
            return json['Sentiment']
        else:
            return None
    def emoticons(json):
        if json and 'emoticons' in json:
            return json['emoticons']
        else:
            return None
    def language_used(json):
        if json and 'language_used' in json:
            return json['language_used']
        else:
            return None
    def postagger(json):
        if json and 'postagger' in json:
            return json['postagger']
        else:
            return None
    def tokenizer(json):
        if json and 'postagger' in json:
            p = [ item[0] for item in json['postagger']]
        else:
            return None
        return p
    def Entities_numeral(json):
        if json and 'Entities_numeral' in json:
            return json['Entities_numeral']
        else:
            return None
    def parser_dependency(json):
        if json and 'parser_dependency' in json:
            return json['parser_dependency']
        else:
            return None
    def get_from_tag(self, json, tag):
        res = []
        if json and 'NLP' in json:
            for item in json['NLP']:
                if 'tag' in item and item['tag'] == tag:
                    res.append(item)
        return res
    def get_verbs(self, json):
        return self.get_from_tag(json, 'VP') + self.get_from_tag(json, 'V')
    def get_nouns(self, json):
        return self.get_from_tag(json, 'N')
    def get_proper_nouns(self, json):
        return self.get_from_tag(json, 'NP')
    def get_adjective(self, json):
        return self.get_from_tag(json, 'JJ')
    def get_numerals(self, json):
        return self.get_from_tag(json, 'CD')
    def get_adverbs(self, json):
        return self.get_from_tag(json, 'RB')
    def get_cls(self, json):
        return self.get_from_tag(json, 'RB')
    def get_clo(self, json):
        return self.get_from_tag(json, 'RB')
    def get_prepositions(self, json):
        return self.get_from_tag(json, 'P')
