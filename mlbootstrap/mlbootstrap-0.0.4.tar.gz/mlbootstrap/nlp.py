import pickle
from typing import Iterable, Callable, Union


class VocabularyProcessor:
    def __init__(self, min_frequency=1):
        """
        The :class:`VocabularyProcessor` builds vocabulary for word tokens.

        Parameters
        ----------
        min_frequency : int
            The minimum word frequency allowed in the vocabulary.
        """
        self.go_token = '<go>'
        self.eos_token = '<eos>'
        self.pad_token = '<pad>'
        self.unk_token = '<unk>'

        self.special_tokens = {
            self.go_token, self.eos_token, self.pad_token, self.unk_token
        }

        self._word2id = {}
        self._id2word = {}
        self._word_frequency = {}
        self._min_frequency = min_frequency

        self.add(self.go_token)
        self.add(self.eos_token)
        self.add(self.pad_token)
        self.add(self.unk_token)

        self.go_id = None
        self.eos_id = None
        self.pad_id = None
        self.unk_id = None

    def size(self):
        """Gets the vocabulary size.

        Returns
        -------
        int
            The vocabulary size, including special tokens.
        """
        return len(self._word2id)

    def add(self, word, frequency=1):
        """Adds a single word token to the vocabulary with the given frequency.

        Parameters
        ----------
        word : str
            The word to add.
        frequency : int
            Add the corresponding word frequency with this value.
        """
        if word in self._word2id:
            self._word_frequency[word] += frequency
        else:
            word_id = len(self._word2id)
            self._word2id[word] = word_id
            self._id2word[word_id] = word
            self._word_frequency[word] = frequency

    def add_all(self, words):
        """Adds all the words to the vocabulary.

        Parameters
        ----------
        words : Iterable
            The words to add.
        """
        for word in words:
            self.add(word)

    def fit(self):
        """Fits the vocabulary."""
        vocab_processor = VocabularyProcessor()
        for word, frequency in self._word_frequency.items():
            if word not in self.special_tokens and frequency >= self._min_frequency:
                vocab_processor.add(word, frequency)

        min_frequency = self._min_frequency
        self.__dict__.update(vocab_processor.__dict__)
        self._min_frequency = min_frequency

        self._word_frequency[self.go_token] = self.size()
        self._word_frequency[self.eos_token] = self.size()
        self._word_frequency[self.pad_token] = self.size()
        self._word_frequency[self.unk_token] = self.size()

        self.go_id = self._word2id[self.go_token]
        self.eos_id = self._word2id[self.eos_token]
        self.pad_id = self._word2id[self.pad_token]
        self.unk_id = self._word2id[self.unk_token]

    def save(self, filename):
        """Saves current vocabulary to binary file with the give filename.

        Parameters
        ----------
        filename : str
            The path to save the vocabulary.
        """
        with open(filename, 'wb') as f:
            pickle.dump(self.__dict__, f, -1)

    def save_text(self, filename):
        """Saves current vocabulary to human readable text.

        Parameters
        ----------
        filename : str
            The path to save the vocabulary.
        """
        with open(filename, 'w') as f:
            for word in self._word2id:
                f.write(word + '\n')

    def restore(self, filename):
        """Restores the vocabulary from the binary file with the given filename.

        Parameters
        ----------
        filename : str
            The path to restore the vocabulary.
        """
        with open(filename, 'rb') as f:
            self.__dict__.update(pickle.load(f))

    def to_id(self, word):
        """Gets the word id of a word.

        Parameters
        ----------
        word : str
            The word token.

        Returns
        -------
        int
            The word id.
        """
        return self._word2id.get(word, self.unk_id)

    def to_word(self, word_id):
        """Gets the word of a word id.

        Parameters
        ----------
        word_id : int
            The word id.

        Returns
        -------
        str
            The word.
        """
        return self._id2word[word_id]

    def word_frequency(self, word):
        """Gets the frequency of a word.

        Parameters
        ----------
        word : str
            The word.

        Returns
        -------
        int
            The word frequency.
        """
        return self._word_frequency[word] if word in self._word2id else 0

    def is_oov(self, word):
        """Checks if a word is an out-of-vocabulary word.

        Parameters
        ----------
        word : str
            The word to check.

        Returns
        -------
        bool
            True if the word is out of vocabulary.
        """
        return word not in self._word2id or word == self.unk_token

    def vectorize_sentence(self,
                           sentence,
                           tokenize_fn=None,
                           add_go_token=False,
                           add_eos_token=False,
                           sentence_length=None):
        """Vectorizes a sentence text.

        Parameters
        ----------
        sentence : Union[str, list of str]
            The sentence text to vectorize.
        tokenize_fn : Callable
            A function that receives a sentence and returns a list of tokens.
        add_go_token : bool
            Whether to add the go token at the first.
        add_eos_token : bool
            Whether to add the eos token at the end.
        sentence_length : int
            The expected sentence length.
            If sentence_length is not None, the missing slots will be padded with pad token,
            no padding otherwise.

        Returns
        -------
        list of int
            The list of word ids.
        """
        if not tokenize_fn:
            tokenize_fn = lambda x: x.split()

        if isinstance(sentence, str):
            sentence = tokenize_fn(sentence)

        if add_go_token:
            sentence = [self.go_token] + sentence
        if add_eos_token:
            sentence = sentence + [self.eos_token]

        if sentence_length is not None:
            n_missing = sentence_length - len(sentence)
            assert n_missing >= 0
            sentence += [self.pad_token] * n_missing

        sentence = [self.to_id(token) for token in sentence]

        return sentence
