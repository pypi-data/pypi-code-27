import io

def read_text(text_path):
    """Reads a text file and converts it to a unicode string.
    
    Arguments:
        text_path {str} -- A path of text file.
    
    Returns:
        [unicode] -- A text file's text as a unicode.
    """
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

def get_unique_characters(text):
    """Extracts unique characters from string.
    
    Arguments:
        text {str} -- A string from which to extract unique characters.
    
    Returns:
        [list] -- A list of unique characters.
    """
    unique_character_set = set(text)
    unique_characters = list(unique_character_set)
    sorted_unique_characters = sorted(unique_characters)
    return sorted_unique_characters