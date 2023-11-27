import unittest
import os
import sys

sys.path.insert(0, "../../src")  # noqa

from create_plots import create_line_plot, create_correlation_matrix
from animal_data import AnimalData  # Import your AnimalData class


class TestCreatePlots(unittest.TestCase):

    # Set up the test cases, with variables paths and data
    def setUp(self):
        # Get data with the AnimalData class
        self.data = AnimalData.from_csv("../../data/4659_aligned_traces.csv")
        self.cells = ["C000", "C001"]
        self.output_file_line = "test_line_plot.png"
        self.output_file_corr = "test_correlation_matrix.png"

    # Check if line plot can be created
    def test_create_line_plot(self):
        create_line_plot(self.data, self.cells, self.output_file_line)
        # Check existence on disk
        self.assertTrue(os.path.exists(self.output_file_line))

    # Check if correlation matrix can be created
    def test_create_correlation_matrix(self):
        create_correlation_matrix(self.data, self.cells, self.output_file_corr)
        self.assertTrue(os.path.exists(self.output_file_corr))

    def tearDown(self):
        # Cleanup, Try to remove the files
        if os.path.exists(self.output_file_line):
            os.remove(self.output_file_line)
        if os.path.exists(self.output_file_corr):
            os.remove(self.output_file_corr)


if __name__ == "__main__":
    unittest.main()
