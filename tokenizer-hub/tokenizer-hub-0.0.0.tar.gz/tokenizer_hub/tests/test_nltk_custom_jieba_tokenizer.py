from unittest import TestCase

from .. import NltkCustomJiebaTokenizer


class NltkCustomJiebaTokenizerTestCase(TestCase):

    def setUp(self):
        self.tokenizer = NltkCustomJiebaTokenizer()

    def test_default_lcut(self):
        tokenizer = NltkCustomJiebaTokenizer()
        self.assertEqual(
            tokenizer.lcut("我想喝Mr.S珍珠奶茶半糖大杯"),
            self.tokenizer.lcut(
                "我想喝Mr.S珍珠奶茶半糖大杯",
                punct=True,
                cut_all=False,
                HMM=False,
            ),
        )
        self.assertEqual(
            ["我", "想", "喝", "Mr", ".", "S", "珍珠奶茶", "半", "糖", "大", "杯"],
            tokenizer.lcut("我想喝Mr.S珍珠奶茶半糖大杯"),
        )

    def test_lcut_punct_false(self):
        tokenizer = NltkCustomJiebaTokenizer(punct=False)
        self.assertEqual(
            tokenizer.lcut("How's it going today, Mr.Smith?"),
            self.tokenizer.lcut(
                "How's it going today, Mr.Smith?",
                punct=False,
            ),
        )
        self.assertEqual(
            ["How", "'s", "it", "going", "today", ",", "Mr.Smith", "?", ],
            tokenizer.lcut("How's it going today, Mr.Smith?"),
        )

    def test_lcut_HMM_false(self):
        tokenizer = NltkCustomJiebaTokenizer(HMM=False)
        self.assertEqual(
            tokenizer.lcut("我想喝Mr.S珍珠奶茶半糖大杯"),
            self.tokenizer.lcut("我想喝Mr.S珍珠奶茶半糖大杯", HMM=False),
        )
        self.assertEqual(
            ["我", "想", "喝", "Mr", ".", "S", "珍珠奶茶", "半", "糖", "大", "杯"],
            tokenizer.lcut("我想喝Mr.S珍珠奶茶半糖大杯"),
        )

    def test_lcut_sentences_parallel(self):
        human_tokened_sentences = [
            ["我", "想", "喝", "珍珠奶茶", "半", "糖", "大", "杯"],
            ["i", "would", "like", "to", "drink", "pearl", "milk", "tea", "."],
            ["_ya_", "我", "想", "喝", "_num_", "杯", "_test_", "飲", "料", "_end_"],
            ["我", "想", "買", "12", "張", "(", "abc", ")", "股"],
            ["我", "想", "買", "12", "張", "abc", "股"],
        ]
        origin_sentences = [
            "我想喝珍珠奶茶半糖大杯",
            "i would like to drink pearl milk tea.",
            "_ya_ 我想喝 _num_ 杯 _test_ 飲料 _end_",
            "我想買12張(abc)股",
            "我想買 12 張 abc 股",
        ]
        tokenized_sentences = self.tokenizer.lcut_sentences(
            origin_sentences,
            num_jobs=8,
            HMM=False,
        )
        self.assertListEqual(human_tokened_sentences, tokenized_sentences)
