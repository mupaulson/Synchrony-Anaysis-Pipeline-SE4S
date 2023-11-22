import unittest
import sys

sys.path.insert(0, '../../src')  # noqa
from animal_data import AnimalData

sys.path.insert(0, '../../src')  # noqa
from load_data import get_args, main

class TestLoadData(unittest.TestCase):
    # === from_csv() ===
    # Positive case for from_csv()
    def test_read_data_from_file(self):
        animal_data = AnimalData.from_csv('../data/4807-test.csv')
        self.assertEqual(animal_data.animal_num, 4807)
        test = animal_data.cell_data["C000"][0]
        self.assertEqual(test, (1657027819.110297, 18.97811))

    # Negative case for read_data_from_file() with nonexistent file
    def test_read_data_from_file_nonexistent(self):
        with self.assertRaises(SystemExit) as cm:
            AnimalData.from_csv('nonexistent.txt')
        self.assertEqual(cm.exception.code, 1)

if __name__ == '__main__':
    unittest.main()