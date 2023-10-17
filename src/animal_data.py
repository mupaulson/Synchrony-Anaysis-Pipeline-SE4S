class AnimalData:
    def __init__(self, animal_num, cell_data):
        self.animal_num = animal_num  # Extracted from the CSV filename
        self.cell_data = cell_data  # Dictionary where keys are cell names, and values are lists of (timestamp, value) tuples

    def get_data_for_cell(self, cell, n = None):
        """Return a list of (timestamp, value) tuples for the specified cell."""
        data = self.cell_data.get(cell, [])
        return data[:n] if n else data

    def get_data_at_time(self, timestamp):
        """Return a dictionary where keys are cells and values are measurements at the specified timestamp."""
        return {cell: next((t, v) for t, v in values if t == timestamp) for cell, values in self.cell_data.items()}

    @classmethod
    def from_csv(cls, filepath):
        """Class method to create an AnimalData instance from a CSV file."""
        import csv

        animal_num = filepath.split('.')[0]

        with open(filepath, 'r') as file:
            reader = csv.reader(file)
            header = next(reader)
            header = [cell.strip() for cell in header]  # This line is added to remove whitespace
            _ = next(reader)  # Skip the cell status row

            cell_data = {cell: [] for cell in header[1:]}

            for row in reader:
                timestamp = float(row[0])
                for i, value in enumerate(row[1:], 1):
                    cell_data[header[i]].append((timestamp, float(value)))

        return cls(animal_num, cell_data)

