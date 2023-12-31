import sys
sys.path.insert(0, '../../src')  # noqa
import df_utils
import normalize_data
from animal_data import AnimalData as ad
import unittest
import numpy as np


class TestNormalize(unittest.TestCase):

    def test_normalize_df(self):
        ani_data = ad.from_csv('../data/4807-test.csv')
        result = normalize_data.normalize_df(ani_data)
        value = int(result.iloc[0, 0])
        m = result.max(axis=0)
        self.assertEqual(m[0], 1.0)
        self.assertEqual(value, 1)

    def test_normalize_df_bad_cells(self):
        ani_data = ad.from_csv('../data/4807-test.csv')
        result = normalize_data.normalize_df(ani_data, cells=[1, 2, 3])
        self.assertIsNone(result)

    #  because we load data into the class structure, can't have value error
