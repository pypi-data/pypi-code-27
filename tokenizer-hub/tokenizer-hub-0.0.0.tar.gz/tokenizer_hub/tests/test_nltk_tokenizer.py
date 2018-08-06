from unittest import TestCase

from .. import NltkTokenizer


class test_NltkTokenizer(TestCase):

    def test_NltkTokenizer(self):
        tokenizer = NltkTokenizer()
        self.assertEqual(
            ['How', "'s", 'it', 'going', 'today', ',', 'Mr.Smith', '?', ],
            tokenizer.lcut("How's it going today, Mr.Smith?", punct=False),
        )
        tokenizer = NltkTokenizer(punct=False)
        self.assertEqual(
            ['How', "'s", 'it', 'going', 'today', ',', 'Mr.Smith', '?', ],
            tokenizer.lcut("How's it going today, Mr.Smith?"),
        )

    def test_NltkTokenizer_punct(self):
        tokenizer = NltkTokenizer()
        self.assertEqual(
            ['How', "'", 's', 'it', 'going', 'today', ',', 'Mr', '.', 'Smith', '?', ],
            tokenizer.lcut("How's it going today, Mr.Smith?", punct=True),
        )
        tokenizer = NltkTokenizer(punct=True)
        self.assertEqual(
            ['How', "'", 's', 'it', 'going', 'today', ',', 'Mr', '.', 'Smith', '?', ],
            tokenizer.lcut("How's it going today, Mr.Smith?"),
        )

    def test_NltkTokenizer_parallel_lcut(self):
        tokenizer = NltkTokenizer()
        human_tokened_sentences = [
            ['How', "'", 's', 'it', 'going', 'today', ',', 'Mr', '.', 'Smith', '?', ],
            ['How', "'", 's', 'it', 'going', 'today', ',', 'Mr', '.', 'John', '?', ],
            ['How', "'", 's', 'it', 'going', 'today', ',', 'Mrs', '.', 'Watson', '?', ],
            ['How', "'", 's', 'it', 'going', 'today', ',', 'Mrs', '.', 'Stone', '?', ],
            ['How', "'", 's', 'it', 'going', 'today', ',', 'Dr', '.', 'Smith', '?', ],
            ['How', "'", 's', 'it', 'going', 'today', ',', 'Dr', '.', 'John', '?', ],
            ['How', "'", 's', 'it', 'going', 'today', ',', 'Mrs', '.', 'Winslet', '?', ],
        ]
        sentences_to_token = [
            "How's it going today, Mr.Smith?",
            "How's it going today, Mr.John?",
            "How's it going today, Mrs.Watson?",
            "How's it going today, Mrs.Stone?",
            "How's it going today, Dr.Smith?",
            "How's it going today, Dr.John?",
            "How's it going today, Mrs.Winslet?",
        ]
        tokenized_sentences = tokenizer.lcut_sentences(
            sentences_to_token,
            num_jobs=4,
            punct=True,
        )
        self.assertListEqual(human_tokened_sentences, tokenized_sentences)
        tokenizer = NltkTokenizer(punct=True)
        tokenized_sentences = tokenizer.lcut_sentences(
            sentences_to_token,
            num_jobs=4,
        )
        self.assertListEqual(human_tokened_sentences, tokenized_sentences)
