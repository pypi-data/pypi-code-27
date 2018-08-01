import re

from typing import List, Tuple

from cnpt.extractor import Extractor
from cnpt.pos_tag import pos_tag
from cnpt.rule import Rule


# 1. Define an extractor

class RegExpExtractor(Extractor):

    def __init__(self, keyword: str, pattern: str):
        super().__init__(keyword)
        self.keyword = keyword
        self.pattern = pattern

    def extract(self, text: str) -> Tuple[str, List[str]]:
        matches = re.findall(self.pattern, text)
        matches = [x[0] for x in matches]
        for m in matches:
            text = text.replace(m, self.keyword, 1)
        return text, matches

greeting_extractor = RegExpExtractor(keyword='GREETING', pattern=r"((Hello|Hi))")


# 2. Define rules

rule = Rule(extractor=greeting_extractor, matches=None)
rules = [rule]


# 3. Use pos_tag to make a tagged words from text

text = 'Hello world!'
tagged_words = pos_tag(text=text, rules=rules)


# 4. See result

print(text)
print(tagged_words)
