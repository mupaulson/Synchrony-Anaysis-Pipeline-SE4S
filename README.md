# Synchrony-Anaysis-Pipeline-SE4S
SE4S 2023 Project

# Normalization and Cell Slicing functions
## v1.0
Implemented:
- created normalize_data.py: takes in animal data and saves a normalized df as a csv
- created cell_slicer.py: takes in correlation matrix df and saves cell pair txt file and df of sorted correlation matrix values
- created df_utils.py: put the function animal_data_to_df from correlation branch here so I can use it too
- created test.ipynb to test all functions in sequence without using snakmake just yet

ToDo:
- create unit and functional tests
- best pratice formatting
- create data saving structure
- snakefile for workflow

# Visualization of Synchrony Analysis Pipeline Part
## v1.0

Implemented:
- create_plots.py: Line plot and correlation plot
- ArgumentParser: Command line interface
- Outputs png files
- Documentation and styleguide follow

ToDO:
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
