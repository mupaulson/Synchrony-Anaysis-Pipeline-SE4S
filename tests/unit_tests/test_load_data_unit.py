import unittest
import sys

sys.path.insert(0, '../../src')  # noqa
from animal_data import AnimalData

sys.path.insert(0, '../../src')  # noqa
from load_data import adjust_timestamps

class LoadDataTests(unittest.TestCase):

    def setUp(self):
        self.animal1 = AnimalData.from_csv("../../data/4659-test2.csv")
        self.animal2 = AnimalData.from_csv("../../data/4807-test2.csv")

        # Perform remapping
        self.animal1.remap_time_values()
        self.animal2.remap_time_values()

    def test_adjust_timestamps(self):
        # Initial test to see if timestamps adjust within the threshold
        adjust_timestamps(self.animal1, self.animal2)

        # Check the first timestamp for a cell
        self.assertEqual(self.animal1.cell_data["C000"][0][0], 0.0)
        self.assertEqual(self.animal2.cell_data["C000"][0][0], 0.0)

    def test_no_adjust_for_large_difference(self):
        # Modify sample data to have a large timestamp difference
        self.animal2.cell_data["C000"][0] = (1.0, self.animal2.cell_data["C000"][0][1])

        adjust_timestamps(self.animal1, self.animal2)

        # Timestamps should remain unchanged because difference is greater than the threshold
        self.assertEqual(self.animal1.cell_data["C000"][0][0], 0.0)
        self.assertEqual(self.animal2.cell_data["C000"][0][0], 1.0)

if __name__ == '__main__':
    unittest.main()
