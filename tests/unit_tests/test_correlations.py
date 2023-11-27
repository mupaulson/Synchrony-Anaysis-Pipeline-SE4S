import unittest
import sys
import pandas as pd

sys.path.insert(0, '../../src')  # noqa
from correlations import correlation_matrix


class TestCorrelations(unittest.TestCase):
    def test_correlations_positive(self):
        df1 = pd.read_csv('../data/correlations_test.csv')
        df2 = df1
        corr_p, corr_r = correlation_matrix(df1, df2)
        self.assertEqual(round(corr_r.loc[' C000', ' C000']), 1)
        self.assertEqual(round(corr_p.loc[' C000', ' C000']), 0)

    # negative test case - make sure data has been processed
    # test for strings in data
    @unittest.expectedFailure
    def test_for_preprocessing(self):
        self.assertRaises('ValueError')
        df1 = pd.read_csv('../data/correlations_test.csv')
        df2 = df1
        correlation_matrix(df1, df2)


if __name__ == '__main__':
    unittest.main()
