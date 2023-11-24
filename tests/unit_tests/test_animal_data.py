import unittest
import sys

sys.path.insert(0, '../../src')  # noqa
from animal_data import AnimalData

sys.path.insert(0, '../../src')  # noqa
from load_data import get_args, main

# === animal_data.py ===
class TestAnimalData(unittest.TestCase):
    # === __init__() ===
    def test_init(self):
        # Positive case: checks AnimalClass constructor
        cell_data = {"C001": [(1, 0.5), (2, 0.6)], "C002": [(1, 0.7), (2, 0.8)]}
        animal = AnimalData(1234, cell_data)
        self.assertEqual(animal.animal_num, 1234)
        self.assertEqual(animal.cell_data, cell_data)

    # === get_data_for_cell() ===
    def test_get_data_for_cell_all(self):
        # Test retrieving all available data for a specific cell.
        cell_data = {"C001": [(1, 0.5), (2, 0.6)]}
        animal = AnimalData(1234, cell_data)
        self.assertEqual(animal.get_data_for_cell("C001"), [(1, 0.5), (2, 0.6)])

    def test_get_data_for_cell_with_n(self):
        # Test retrieving limited data (n elements) for a specific cell.
        cell_data = {"C001": [(1, 0.5), (2, 0.6)]}
        animal = AnimalData(1234, cell_data)
        self.assertEqual(animal.get_data_for_cell("C001", 1), [(1, 0.5)])

    def test_get_data_for_cell_nonexistent(self):
        # Test retrieving data for a cell that doesn't exist (should return empty list).
        animal = AnimalData(1234, {})
        self.assertEqual(animal.get_data_for_cell("C999"), [])

    # === get_data_at_time() ===
    def test_get_data_at_time(self):
        # Test retrieving data for all cells at a specific timestamp.
        cell_data = {"C001": [(1, 0.5)], "C002": [(1, 0.7), (2, 0.8)]}
        animal = AnimalData(1234, cell_data)
        expected = {"C001": (1, 0.5), "C002": (1, 0.7)}
        self.assertEqual(animal.get_data_at_time(1), expected)

    def test_get_data_at_time_nonexistent(self):
        # Test retrieving data at a timestamp that does not exist (should return None for all cells).
        cell_data = {"C001": [(1, 0.5)], "C002": [(2, 0.8)]}
        animal = AnimalData(1234, cell_data)
        expected = {"C001": (None, None), "C002": (None, None)}
        self.assertEqual(animal.get_data_at_time(3), expected)

    # === from_csv() ===
    def test_read_data_from_file(self):
        # Positive case for from_csv()
        animal_data = AnimalData.from_csv('../data/4807-test.csv')
        self.assertEqual(animal_data.animal_num, 4807)
        test = animal_data.cell_data["C000"][0]
        self.assertEqual(test, (1657027819.110297, 0.0, 18.97811))

    def test_read_data_from_file_nonexistent(self):
        # Negative case for read_data_from_file() with nonexistent file
        with self.assertRaises(SystemExit) as cm:
            AnimalData.from_csv('nonexistent.txt')
        self.assertEqual(cm.exception.code, 1)

if __name__ == '__main__':
    unittest.main()