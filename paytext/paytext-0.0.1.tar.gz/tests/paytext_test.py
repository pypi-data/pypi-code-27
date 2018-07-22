# pyre-strict

"""
This is the main test file for the paytext module.
"""

import unittest
from typing import List, Dict
from paytext import PaymentText

EXAMPLE_TEXTS: List[Dict[str, str]] = [
    {
        'input': '',
        'expected_output': '',
    },
    {
        'input': 'COINBASE UK, LTD                   EUR              15,94',
        'expected_output': 'COINBASE UK, LTD',
    },
    {
        'input': 'COINBASE UK, LTD                   EUR              182,12',
        'expected_output': 'COINBASE UK, LTD',
    },
    {
        'input': 'Fra: Solan Gundersen 18.06.18',
        'expected_output': 'Fra: Solan Gundersen',
    },
    {
        'input': '*4274 25.06 NOK 4101.00 WWW.TICKET.NO Kurs: 1.0000',
        'expected_output': 'WWW.TICKET.NO',
    },
    {
        'input': 'OBOS FACTORING',
        'expected_output': 'OBOS FACTORING',
    },
    {
        'input': '30.06 COOP PRIX VG-HU AKERSGT 55 OSLO',
        'expected_output': 'COOP PRIX VG-HU AKERSGT 55 OSLO',
    },
    {
        'input': '*8877 01.07 USD 12.99 IRRADIATED SOFTWARE Kurs: 8.3718',
        'expected_output': 'IRRADIATED SOFTWARE',
    },
    {
        'input': '*3951 01.07 EUR 4.00 GOOGLE *SVCSAPPS_hoise Kurs: 9.7250',
        'expected_output': 'GOOGLE *SVCSAPPS_hoise',
    },
    {
        'input': '*9090 29.06 USD 1.00 SAM HARRIS MEDIA INC Kurs: 8.3700',
        'expected_output': 'SAM HARRIS MEDIA INC',
    },
    {
        'input': '05.07 KIWI 471 BISLET THERESESGT 3 OSLO',
        'expected_output': 'KIWI 471 BISLET THERESESGT 3 OSLO',
    },
    {
        'input': '04.07 DEN NORSKE TURISTFOR. OSLO',
        'expected_output': 'DEN NORSKE TURISTFOR. OSLO',
    },
    {
        'input': 'Nettgiro til: Universitetet i Betalt: 05.07.18',
        'expected_output': 'Nettgiro til: Universitetet i',
    },
    {
        'input': '05.07 REMA SANNERGATA SANNERGATA 3 OSLO',
        'expected_output': 'REMA SANNERGATA SANNERGATA 3 OSLO',
    },
    {
        'input': 'Vipps',
        'expected_output': 'Vipps',
    },
    {
        'input': '04.07 SKOM.DAGESTAD JOSEFINEGT.  OSLO',
        'expected_output': 'SKOM.DAGESTAD JOSEFINEGT. OSLO',
    },
    {
        'input': '*4321 29.06 USD 50.00 ITUNES.COM/BILL Rate: 1.0000',
        'expected_output': 'ITUNES.COM/BILL',
    },
    {
        'input': '*1234 01.07 NOK 215.00 ITUNES.COM/BILL Kurs: 1.0000',
        'expected_output': 'ITUNES.COM/BILL',
    },
]


class PaymentTextTest(unittest.TestCase):
    """
    This is the test class for the PaymentText class.
    """
    def test_generalize(self) -> None:
        """
        Test that PaymentText.generalize() properly cleans a payment text.

        :return:
        """
        for example_text in EXAMPLE_TEXTS:
            text = PaymentText(example_text['input'])

            text.generalize()

            self.assertEqual(
                str(text),
                example_text['expected_output'],
            )


if __name__ == '__main__':
    unittest.main()
