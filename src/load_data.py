from animal_data import AnimalData

# Create an instance from the CSV
animal_data = AnimalData.from_csv('../data/test.csv')

# Get data for a specific cell
print(animal_data.get_data_for_cell('C000', 10))

# Get data for all cells at a specific timestamp
print(animal_data.get_data_at_time(1650475072.560337))
