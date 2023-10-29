from animal_data import AnimalData

def main():
    # Load CSVs
    animal1_data = AnimalData.from_csv("../data/4659-test2.csv")
    animal2_data = AnimalData.from_csv("../data/4807-test2.csv")

    # Adjust their timestamps
    animal1_data.remap_time_values()
    animal2_data.remap_time_values()

    # Save time adjusted datasets
    animal1_data.save_to_csv("../data/4659-test2-remap.csv")
    animal2_data.save_to_csv("../data/4807-test2-remap.csv")

    print("CSVs remapped and saved successfully.")

if __name__ == "__main__":
    main()