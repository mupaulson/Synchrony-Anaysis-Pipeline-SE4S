# Synchrony-Anaysis-Pipeline-SE4S
SE4S 2023 Project

# Normalization and Cell Slicing functions
## v1.0
Implemented:
- created normalize_data.py: takes in animal data and saves a normalized df as a csv
- created cell_slicer.py: takes in correlation matrix df and saves cell pair txt file and df of sorted correlation matrix values
- created df_utils.py: put the function animal_data_to_df from correlation branch here so I can use it too

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
