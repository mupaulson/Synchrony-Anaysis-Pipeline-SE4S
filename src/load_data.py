from animal_data import AnimalData

# # Create an instance from the CSV
# animal_data = AnimalData.from_csv('../data/4659-test1.csv')

animal_data = AnimalData.from_csv_and_remap("../data/4659-test1.csv")
animal_data.save_to_csv("../data/4659-test1.csv")

# Get data for a specific cell
print(animal_data.get_data_for_cell('C000', 10))

# Get data for all cells at a specific timestamp
print(animal_data.get_data_at_time(1650475072.560337))
