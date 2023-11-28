import pandas as pd
import numpy as np
from animal_data import AnimalData as ad


#  MP:this function from the correlation file should prob be in a utilities python notebook becuase I will also need it
# uses AnimalData class to access data from a list of cells and returns a dataframe across all timepoints
def animal_data_to_df(data, cells):
    df = pd.DataFrame(data=[],columns=cells)
    try:
        for c in cells:
            t = data.get_data_for_cell(c)
            time, elapsed_time, cell =  map(list,zip(*t))
            df[c] = cell

        return df
    except ValueError:
        print('cells are not correctly named')
        return None
