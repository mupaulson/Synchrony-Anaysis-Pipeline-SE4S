# Synchrony-Anaysis-Pipeline-SE4S

SE4S 2023

Team Members: Maya Paulson, Emma Keppler, Deanna Gelosi, and Philipp Wunsch 

## v1.0

### Data Loader

**Implemented**

- AnimalData class that reads CSV files and outputs a list of Tuples for each cell
- Function `get_data_for_cell()` to return specified cell data
- Function `get_data_at_time()` to return all cell data at specified time
- Function `remap_time_values()` starts time at 0.00 seconds and rounds all time values to nearest 1/100 second
- Function `save_to_csv()` saves the AnimalData class object to a new CSV file
- Function `from_csv()` loads initial CSV file into an AnimalData class object
- Unit and functional testing for loading CSV
- Setup continuous integration yaml file for unit and functional tests

**ToDo**

- Additional unit and functional testing for `animal_data.py` and `load_data.py`
- NAN if no cell value (numpy)
- Run pylint style tests
- Enable style tests in continuous integration

### Normalization and Cell Slicing functions

**Implemented**

- created normalize_data.py: takes in animal data and saves a normalized df as a csv
- created cell_slicer.py: takes in correlation matrix df and saves cell pair txt file and df of sorted correlation matrix values
- created df_utils.py: put the function animal_data_to_df from correlation branch here so I can use it too
- created test.ipynb to test all functions in sequence without using snakmake just yet

**ToDo**

- create unit and functional tests
- best pratice formatting
- create data saving structure
- snakefile for workflow

### Visualization of Synchrony Analysis Pipeline Part

**Implemented**

- create_plots.py: Line plot and correlation plot
- ArgumentParser: Command line interface
- Outputs png files
- Documentation and styleguide follow

**ToDo**

- Create unit tests for each function
- Create functional tests
- Handle exceptions




## Testing

### Unit Tests

1. Move into the unit_test directory.

    ```bash
    cd tests/unit_tests
    ```

2. Run unit tests.

   ```bash
   python3 -m unittest test_animal_data.py  
   ```

### Functional Tests

1. Move into the functional_test directory.

    ```bash
    cd tests/functional_tests
    ```

2. Run functional tests.

    ```bash
    chmod +x test_load_data.sh
    ./test_load_data.sh 
    ```
