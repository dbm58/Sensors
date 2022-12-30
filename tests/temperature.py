#!/usr/bin/env python

import unittest

from lib2 import Temperature

class TestTemperature(unittest.TestCase):

    def test_formatter(self):
        temp = Temperature(12.345)
        self.assertEqual(f'{temp}',      '12.345')
        self.assertEqual(f'{temp:.1}',   '12.3')
        self.assertEqual(f'{temp:.2}',   '12.35')
        self.assertEqual(f'{temp:.3}',   '12.345')
        self.assertEqual(f'{temp:.4}',   '12.3450')
        self.assertEqual(f'{temp:1.3}',  '12.345')
        self.assertEqual(f'{temp:2.3}',  '12.345')
        self.assertEqual(f'{temp:3.3}',  '12.345')
        self.assertEqual(f'{temp:4.3}',  '12.345')
        self.assertEqual(f'{temp:5.3}',  '12.345')
        self.assertEqual(f'{temp:6.3}',  '12.345')
        self.assertEqual(f'{temp:7.3}',  ' 12.345')
        self.assertEqual(f'{temp:.1C}',  '12.3\N{DEGREE SIGN}C')
        self.assertEqual(f'{temp:.1c}',  '12.3\N{DEGREE SIGN}c')
        self.assertEqual(f'{temp:.2C}',  '12.35\N{DEGREE SIGN}C')
        self.assertEqual(f'{temp:.3C}',  '12.345\N{DEGREE SIGN}C')
        self.assertEqual(f'{temp:1.3C}', '12.345\N{DEGREE SIGN}C')
        self.assertEqual(f'{temp:2.3C}', '12.345\N{DEGREE SIGN}C')
        self.assertEqual(f'{temp:7.3C}', ' 12.345\N{DEGREE SIGN}C')
        self.assertEqual(f'{temp:8.3C}', '  12.345\N{DEGREE SIGN}C')
        self.assertEqual(f'{temp:9.3C}', '   12.345\N{DEGREE SIGN}C')
        self.assertEqual(f'{temp:.1F}',  '54.2\N{DEGREE SIGN}F')
        self.assertEqual(f'{temp:.1f}',  '54.2\N{DEGREE SIGN}f')
        self.assertEqual(f'{temp:.2f}',  '54.22\N{DEGREE SIGN}f')
        self.assertEqual(f'{temp:.3f}',  '54.221\N{DEGREE SIGN}f')

if __name__ == '__main__':
    unittest.main()
