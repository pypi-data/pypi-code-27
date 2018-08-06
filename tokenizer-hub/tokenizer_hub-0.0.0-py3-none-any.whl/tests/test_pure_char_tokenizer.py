# -*- coding: utf-8 -*-
from unittest import TestCase

from ..pure_char_tokenizer import (
    CharTokenizerForPureWords,
    PureChineseCharTokenizer,
)


class PureCharTokenizerTestCase(TestCase):

    def setUp(self):
        self.tokenizer = CharTokenizerForPureWords()
        self.pure_tokenizer = PureChineseCharTokenizer()

    def test_char_tokenizer(self):
        test_cases = [
            ("#abcAWERDFTQookirh09875462512k.-(){}[]#@!~<>=*^|_%:;?",
             ["#abcAWERDFTQookirh09875462512k.-(){}[]#@!~<>=*^|_%:;?"]),
            ("我想要買miss.M的蛋糕", ["我", "想", "要", "買", "miss.M", "的", "蛋", "糕"]),
            ("來一卡車MM chocolate", ["來", "一", "卡", "車", "MM chocolate"]),
            ("想要買(B)股", ["想", "要", "買", "(B)", "股"]),
            ("來一杯40.77度的pink lady",
             ["來", "一", "杯", "40.77", "度", "的", "pink lady"]),
            ("薄餡的手機號碼是0800-000-123",
             ["薄", "餡", "的", "手", "機", "號", "碼", "是", "0800-000-123"]),
        ]
        for test_case in test_cases:
            with self.subTest(test_case=test_case):
                self.assertEqual(
                    test_case[1],
                    self.tokenizer.lcut(test_case[0]),
                )

    def test_char_tokenizer_parallel(self):
        actual_result = self.tokenizer.lcut_sentences(
            sentences=[
                "#abcAWERDFTQookirh09875462512k.-(){}[]#@!~<>=*^|_%:;?",
                "我想要買miss.M的蛋糕",
                "來一卡車MM chocolate",
                "想要買(B)股",
                "來一杯40.77度的pink lady",
                "薄餡的手機號碼是0800-000-123",
            ],
        )
        self.assertEqual(
            [
                ["#abcAWERDFTQookirh09875462512k.-(){}[]#@!~<>=*^|_%:;?"],
                ["我", "想", "要", "買", "miss.M", "的", "蛋", "糕"],
                ["來", "一", "卡", "車", "MM chocolate"],
                ["想", "要", "買", "(B)", "股"],
                ["來", "一", "杯", "40.77", "度", "的", "pink lady"],
                ["薄", "餡", "的", "手", "機", "號", "碼", "是", "0800-000-123"],
            ],
            actual_result,
        )

    def test_pure_chinese_char_tokenizer(self):
        test_cases = [
            ("我想要買miss.M的蛋糕", ['我', '想', '要',
                               '買', 'miss', 'm', '的', '蛋', '糕']),
            ("來一卡車mm chocolate<><>!!!###", [
             '來', '一', '卡', '車', 'mm', 'chocolate']),
            ("想要買(B)股", ["想", "要", "買", "b", "股"]),
            ("來一杯40.77度的pink lady",
             ["來", "一", "杯", "40", "77", "度", "的", "pink", "lady"]),
            ("薄餡的手機號碼是0800-000-123",
             ["薄", "餡", "的", "手", "機", "號", "碼", "是", "_phone_"]),
            ("豪大大想買100個豪大大雞排",
             ["豪", "大", "大", "想", "買", "_num_", "個", "豪", "大", "大", "雞", "排"]),
        ]
        for test_case in test_cases:
            with self.subTest(test_case=test_case):
                self.assertEqual(
                    test_case[1],
                    self.pure_tokenizer.lcut(test_case[0]),
                )
