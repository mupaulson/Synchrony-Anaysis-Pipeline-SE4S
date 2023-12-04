# example script to generate corralations
from animal_data import AnimalData as ad
import df_utils as utils
import correlations as corr
from normalize_data import normalize_df


# get the animal data as class
animal_data1 = ad.from_csv('../data/4659_aligned_traces.csv')
animal_data2 = ad.from_csv('../data/4807_aligned_traces.csv')

# make 2 normalized dataframes for analysis
df1 = normalize_df(animal_data1)
df2 = normalize_df(animal_data2)

# Output 2 dataframes for p and R values
p_data, r_data = corr.correlation_matrix(df1, df2)
p_data.to_csv('test.csv')
