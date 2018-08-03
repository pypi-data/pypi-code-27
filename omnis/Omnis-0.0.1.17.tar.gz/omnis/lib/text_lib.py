import io

def read_text(text_path):
    text = io.open(text_path, encoding='utf-8').read()
    return text

def parse_sentences_and_next_characters(whole_text, max_sentence_size, interval_between_each_sentence):
    sentences = []
    next_characters = []
    for i in range(0, len(whole_text) - max_sentence_size, interval_between_each_sentence):
        sentence = whole_text[i: i + max_sentence_size]
        sentences.append(sentence)
        next_character_of_sentence = whole_text[i + max_sentence_size]
        next_characters.append(next_character_of_sentence)
    return sentences, next_characters