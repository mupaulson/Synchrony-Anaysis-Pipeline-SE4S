import sys
sys.path.insert(0, '../../src')  # noqa
import cell_slicer
import unittest
import random
import pandas as pd
import os


class TestSlicer(unittest.TestCase):
    # def setUp(self):
    #     file = '../data/random_r_matrix.csv'
    #     rdf = pd.read_csv(file, index_col=0)
    #     pfile = '../data/random_r_matrix.csv'
    #     pdf = pd.read_csv(pfile, index_col=0)
    #     sig_file = '../data/fake_sig_p_matrix.csv'
    #     sdf = pd.read_csv(sig_file, index_col=0)

    #  testing correct use cases
    def test_cell_query_top(self):
        file = '../data/random_r_matrix.csv'
        rdf = pd.read_csv(file, index_col=0)
        cell_pairs, sorted_matrix, n = cell_slicer.cell_query(rdf,
                                                              'top',
                                                              x_percent=20)
        pair_len = len(cell_pairs)  # should be 2 for rounded 9*0.2
        value = sorted_matrix[0]
        max_values = rdf.max()  # change to axis=None for pd v2.0 to get scalar

        self.assertEqual(pair_len, 2)
        self.assertEqual(value, max_values[0])
        self.assertIsNone(n)

    def test_cell_query_sig(self):
        file = '../data/random_r_matrix.csv'
        rdf = pd.read_csv(file, index_col=0)
        sig_file = '../data/fake_sig_p_matrix.csv'
        sdf = pd.read_csv(sig_file, index_col=0)
        cell_pairs, sorted_matrix, p_matrix = cell_slicer.cell_query(rdf,
                                                                     'sig',
                                                                     p_data=sdf)  # noqa
        pair_len = len(cell_pairs)
        value1 = sorted_matrix[0]
        value2 = p_matrix[0]
        max_values = rdf.max()
        min_values = sdf.min()

        self.assertEqual(pair_len, 6)
        self.assertEqual(value1, max_values[0])
        self.assertEqual(value2, min_values[1])

    #  testing errors
    def test_cell_query_bad_args(self):
        file = '../data/random_r_matrix.csv'
        rdf = pd.read_csv(file, index_col=0)
        test1 = cell_slicer.cell_query(rdf, 'percent')
        test2 = cell_slicer.cell_query(rdf, 'sig')
        test3 = cell_slicer.cell_query(rdf, 'top')

        self.assertIsNone(test1)
        self.assertIsNone(test2)
        self.assertIsNone(test3)

    def test_cell_query_bad_data(self):
        file = '../data/random_r_matrix.csv'
        rdf = pd.read_csv(file, index_col=0)
        file2 = '../data/string_matrix.csv'
        string_df = pd.read_csv(file2, index_col=0)
        test1 = cell_slicer.cell_query(string_df, 'top', x_percent=20)
        test2 = cell_slicer.cell_query(rdf, 'sig', p_data=string_df)

        self.assertIsNone(test1)
        self.assertIsNone(test2)

    #  Edge cases
    def test_cell_query_no_sig_values(self):
        file = '../data/random_r_matrix.csv'
        rdf = pd.read_csv(file, index_col=0)
        pfile = '../data/random_p_matrix.csv'
        pdf = pd.read_csv(pfile, index_col=0)
        cell_pairs, sorted_matrix, p_matrix = cell_slicer.cell_query(rdf,
                                                                     'sig',
                                                                     p_data=pdf)  # noqa
        pair_len = len(cell_pairs)
        value = p_matrix[0]
        min_values = pdf.min()

        self.assertEqual(pair_len, 0)
        self.assertEqual(value, min_values[0])

    def test_cell_query_top_tiny_percent(self):
        file = '../data/random_r_matrix.csv'
        rdf = pd.read_csv(file, index_col=0)
        cell_pairs, sorted_matrix, n = cell_slicer.cell_query(rdf,
                                                              'top',
                                                              x_percent=1)
        pair_len = len(cell_pairs)  # 1% rounded is 0
        value = sorted_matrix[0]
        max_values = rdf.max()  # change to axis=None for pd v2.0 to get scalar

        self.assertEqual(pair_len, 0)
        self.assertEqual(value, max_values[0])
        self.assertIsNone(n)
