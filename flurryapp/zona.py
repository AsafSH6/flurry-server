import pandas as pd

df = pd.DataFrame({'bob': [1, 0, 1, 1], 'bop': [1, 1, 0, 0], 'stm': [1, 0, 0, 1]})

row = 'bob'

rows_true_df = df[df[row] == True]

print df.ix[rows_true_df.sum(axis=1).idxmin()]


