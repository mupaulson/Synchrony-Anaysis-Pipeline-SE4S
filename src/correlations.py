import pandas as pd
import numpy as np
import scipy.stats as sps
from animal_data import AnimalData as ad

# uses AnimalData class to access data from a list of cells and returns a dataframe across all timepoints
def animal_data_to_df(data, cells):
    df = pd.DataFrame(data=[],columns=cells)

    for c in cells:
        t = data.get_data_for_cell(c)
        time,cell =  map(list,zip(*test))
        df[c] = cell
        
    return df


# correlations - requires 2 dataframes and uses scipy correlate to correlate all cell values in the dataframes
# returns 2 dataframes - corr coef and p-values
def correlation_matrix(dataframe1, dataframe2):
   
    col1 = [c for c in data1.columns.values]
    col2 = [c for c in data2.columns.values]

    #convert columns to numpy to correlate
    #if all values in the column are the same NaN values will be returned
    corr_p = pd.DataFrame(data=[],index = col1, columns = col2)
    corr_r = pd.DataFrame(data=[],index = col1, columns = col2)
    
    for c1 in col1:
        for c2 in col2:
            a1 = data1[c1].astype(float)
            a2 = data2[c2].astype(float)
            (p,r) = sps.pearsonr(a1,a2)
            
            corr_p.loc[c1,c2] = p
            corr_r.loc[c1,c2] = r
            
    return corr_p, corr_r