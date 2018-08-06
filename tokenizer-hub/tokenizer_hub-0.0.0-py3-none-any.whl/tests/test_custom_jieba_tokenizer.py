from unittest import TestCase

from .. import CustomJiebaTokenizer
from ..add_words import AddWords


class CustomJiebaTokenizerTestCase(TestCase):

    def setUp(self):
        self.tokenizer = CustomJiebaTokenizer()

    def test_default_lcut(self):
        self.assertEqual(
            self.tokenizer.lcut("我想喝珍珠奶茶半糖大杯"),
            self.tokenizer.lcut(
                "我想喝珍珠奶茶半糖大杯",
                cut_all=False,
                HMM=False,
            ),
        )
        self.assertEqual(
            ["我", "想", "喝", "珍珠奶茶", "半", "糖", "大", "杯"],
            self.tokenizer.lcut("我想喝珍珠奶茶半糖大杯"),
        )

    def test_hmm_true(self):
        tokenizer = CustomJiebaTokenizer(HMM=True)
        self.assertEqual(
            tokenizer.lcut("我想喝珍珠奶茶半糖大杯"),
            self.tokenizer.lcut("我想喝珍珠奶茶半糖大杯", HMM=True),
        )
        self.assertEqual(
            ["我", "想", "喝", "珍珠奶茶", "半糖", "大杯"],
            tokenizer.lcut("我想喝珍珠奶茶半糖大杯"),
        )

    def test_cut_all_true(self):
        tokenizer = CustomJiebaTokenizer(cut_all=True)
        self.assertEqual(
            tokenizer.lcut("我想喝珍珠奶茶半糖大杯"),
            self.tokenizer.lcut("我想喝珍珠奶茶半糖大杯", cut_all=True),
        )
        self.assertEqual(
            ["我", "想", "喝", "珍珠", "珍珠奶茶", "奶茶", "半", "糖", "大杯"],
            self.tokenizer.lcut("我想喝珍珠奶茶半糖大杯", cut_all=True),
        )

    def test_lcut_with_extra_words(self):
        sentence = "我想吃珍珠奶茶鍋，加一道普羅旺斯主廚香煎烤雞排"
        extra_words = ["珍珠奶茶鍋", "普羅旺斯主廚香煎烤雞排"]
        expected_tokens = ["我", "想", "吃", "珍珠奶茶鍋",
                           "，", "加", "一道", "普羅旺斯主廚香煎烤雞排"]
        with AddWords(tokenizer=self.tokenizer, extra_words=extra_words):
            actual_tokens = self.tokenizer.lcut(sentence)
        self.assertEqual(expected_tokens, actual_tokens)

    def test_no_side_effects_after_lcut(self):
        sentence = "我想吃珍珠奶茶鍋，加一道普羅旺斯主廚香煎烤雞排"
        extra_words = ["珍珠奶茶鍋", "普羅旺斯主廚香煎烤雞排"]
        old_result = self.tokenizer.lcut(sentence)
        with AddWords(tokenizer=self.tokenizer, extra_words=extra_words):
            self.tokenizer.lcut(sentence)
        new_result = self.tokenizer.lcut(sentence)
        self.assertEqual(old_result, new_result)

    def test_lcut_sentences_parallel(self):
        human_tokened_sentences = [
            ["我", "想", "喝", "珍珠奶茶", "半", "糖", "大", "杯"],
            ["你", "想", "喝", "珍珠奶茶", "半", "糖", "小杯"],
            ["他", "想", "喝", "珍珠奶茶", "全", "糖", "大", "杯"],
            ["她", "想", "喝", "珍珠奶茶", "半", "糖", "大", "杯"],
            ["我", "想", "喝", "珍珠奶茶", "半", "糖", "中", "杯"],
        ]
        origin_sentences = [
            "我想喝珍珠奶茶半糖大杯",
            "你想喝珍珠奶茶半糖小杯",
            "他想喝珍珠奶茶全糖大杯",
            "她想喝珍珠奶茶半糖大杯",
            "我想喝珍珠奶茶半糖中杯",
        ]
        tokenized_sentences = self.tokenizer.lcut_sentences(
            origin_sentences,
            num_jobs=8,
            HMM=False,
        )
        self.assertListEqual(human_tokened_sentences, tokenized_sentences)
