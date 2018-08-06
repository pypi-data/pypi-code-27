# -*- coding: utf-8 -*-
from unittest import TestCase

from ..chinese_char_tokenizer import (
    ChineseCharTokenizer,
)


class ChineseCharTokenizerTestCase(TestCase):

    def setUp(self):
        self.tokenizer = ChineseCharTokenizer()

    def test_chinese_char_tokenizer(self):
        test_cases = [
            ("我想要買miss.M的蛋糕", ["我", "想", "要", "買",
                               "miss", ".", "M", "的", "蛋", "糕"]),
            ("來一卡車MM chocolate", ["來", "一", "卡", "車", "MM", " ", "chocolate"]),
            ("想要買(B)股", ["想", "要", "買", "(", "B", ")", "股"]),
            ("來一杯40.77度的pink lady",
             ["來", "一", "杯", "40.77", "度", "的", "pink", " ", "lady"]),
            ("來一杯_float_度的pink lady",
             ["來", "一", "杯", "_float_", "度", "的", "pink", " ", "lady"]),
            ("_3float2_元的飲料", ["_3float2_", "元", "的", "飲", "料"]),
            ("I want _12int_ cup of bubble tea",
             ["I", " ", "want", " ", "_12int_", " ", "cup", " ", "of", " ", "bubble", " ", "tea"]),
            ("薄餡的手機號碼是0800-000-123",
             ["薄", "餡", "的", "手", "機", "號", "碼", "是", "0800", "-", "000", "-", "123"]),
            ("邊...邊緣人", ["邊", "...", "邊", "緣", "人"]),
        ]
        for test_case in test_cases:
            with self.subTest(test_case=test_case):
                self.assertEqual(
                    test_case[1],
                    self.tokenizer.lcut(test_case[0]),
                )

    def test_chinese_char_tokenizer_parallel(self):
        actual_result = self.tokenizer.lcut_sentences(
            sentences=[
                "我想要買miss.M的蛋糕",
                "來一卡車MM chocolate",
                "想要買(B)股",
                "來一杯40.77度的pink lady",
                "來一杯_float_度的pink lady",
                "_3float2_元的飲料",
                "I want _12int_ cup of bubble tea",
                "薄餡的手機號碼是0800-000-123",
            ],
        )
        self.assertEqual(
            [
                ["我", "想", "要", "買", "miss", ".", "M", "的", "蛋", "糕"],
                ["來", "一", "卡", "車", "MM", " ", "chocolate"],
                ["想", "要", "買", "(", "B", ")", "股"],
                ["來", "一", "杯", "40.77", "度", "的", "pink", " ", "lady"],
                ["來", "一", "杯", "_float_", "度", "的", "pink", " ", "lady"],
                ["_3float2_", "元", "的", "飲", "料"],
                ["I", " ", "want", " ", "_12int_", " ", "cup",
                 " ", "of", " ", "bubble", " ", "tea"],
                ["薄", "餡", "的", "手", "機", "號", "碼", "是",
                 "0800", "-", "000", "-", "123"],
            ],
            actual_result,
        )
