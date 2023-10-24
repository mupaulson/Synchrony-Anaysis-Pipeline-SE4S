#example script to generate corralations
from animal_data import AnimalData as ad
import correlations as corr

#get the animal data as class
animal_data = ad.from_csv('../data/test.csv')
#define cells to make into dataframe for correlations
col1 = ['C000', 'C001']
col2 = ['C002']

#make 2 dataframes for analysis
df1 = corr.animal_data_to_df(animal_data,col1)
df2 = corr.animal_data_to_df(animal_data,col2)

#Output 2 dataframes for p and R values
p_data,r_data = corr.correlation_matrix(df1,df2)
