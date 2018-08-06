from unittest import TestCase

from .. import PureWordsTokenizer


class PurewordsTokenizerTestCase(TestCase):

    def setUp(self):
        self.tokenizer = PureWordsTokenizer()

    def test_lcut(self):
        test_cases = [
            {
                "sentence": "薄餡=柏憲=cph=cph_is_god\n讚讚讚！聯絡方式：cph@cph.tw, 0912345678",
                "answer": ['薄餡', '柏憲', 'cph', 'cph', 'is', 'god',
                           '讚', '讚', '讚', '聯絡', '方式', '_url_', '_phone_'],
            },
            {
                "sentence": "_薄餡=柏憲=cph=cph_is_god\n讚讚讚！聯絡方式：cph@cph.tw, __0912345678_",
                "answer": ['薄餡', '柏憲', 'cph', 'cph', 'is', 'god',
                           '讚', '讚', '讚', '聯絡', '方式', '_url_', '_phone_'],
            },
            {
                "sentence": "_ _ _ _ _ ",
                "answer": [],
            },
            {
                "sentence": "__ ____ _ _ _ ",
                "answer": [],
            },
        ]
        for test_case in test_cases:
            with self.subTest(test_case=test_case):
                self.assertEqual(
                    test_case['answer'],
                    self.tokenizer.lcut(sentence=test_case['sentence']),
                )
