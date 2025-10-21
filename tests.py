#!/usr/bin/env python3
# SPDX-License-Identifier: MIT

import unittest

from terbilang import Terbilang


class TestTerbilang(unittest.TestCase):
    def setUp(self):
        print('\r\n[', self.id(), ']')

        self.t = Terbilang()

    def test_basic(self):
        words = ('nol', 'satu', 'dua', 'tiga', 'empat', 'lima', 'enam',
                 'tujuh', 'delapan', 'sembilan', 'sepuluh', 'sebelas',
                 'dua belas')

        for num, word in enumerate(words):
            self.t.parse(num)
            self.assertEqual(self.t.getresult(), word)

        self.t.parse('1100')
        self.assertEqual(self.t.getresult(), 'seribu seratus')

        self.t.parse('200001')
        self.assertEqual(self.t.getresult(), 'dua ratus ribu satu')

        self.t.parse('1001')
        self.assertEqual(self.t.getresult(), 'seribu satu')

        self.t.parse('21001')
        self.assertEqual(self.t.getresult(), 'dua puluh satu ribu satu')

    def test_large_numbers(self):
        self.t.parse('1000000000')
        self.assertEqual(self.t.getresult(), 'satu miliar')

        self.t.parse('11000000000000000')
        self.assertEqual(self.t.getresult(), 'sebelas ribu triliun')

        self.t.parse('19000000000000000000071000102011000210')
        self.assertEqual(
            'sembilan belas undesiliun, tujuh puluh satu ribu triliun, '
            'seratus dua miliar sebelas juta dua ratus sepuluh',
            self.t.getresult()
        )

    def test_negative_numbers(self):
        self.t.parse('-1,0')
        self.assertEqual(self.t.getresult(), 'minus satu koma nol')

    def test_separator(self):
        self.t.parse('1.000,00')
        self.assertEqual(self.t.getresult(), 'seribu koma nol nol')

        t = Terbilang('1000.00', sep='.')
        self.assertEqual(t.getresult(), 'seribu koma nol nol')

    def test_separator_autodetect(self):
        self.t.parse('0,1')
        self.assertEqual(self.t.getresult(), 'nol koma satu')

        self.t.parse('0.1')
        self.assertEqual(self.t.getresult(), 'nol koma satu')

        self.t.parse('1,000')
        self.assertEqual(self.t.getresult(), 'satu koma nol nol nol')

        self.t.parse('1.00')
        self.assertEqual(self.t.getresult(), 'satu koma nol nol')

        self.t.parse('1.000')
        self.assertEqual(self.t.getresult(), 'seribu')

    def test_invalid_separator(self):
        with self.assertRaises(ValueError):
            self.t.parse(sep=';')

    def test_too_large(self):
        with self.assertRaises(ValueError):
            self.t.parse('9' * 73)

    def test_empty(self):
        self.t.parse('')
        self.assertEqual(self.t.getresult(), '')


if __name__ == '__main__':
    unittest.main()
