from pathlib import Path
import pandas as pd

path_sp = Path.cwd().parent.joinpath('data').joinpath('sp500.parquet')
path_ff = Path.cwd().parent.joinpath('data').joinpath('ff_factors.parquet')

sp_df = pd.read_parquet(path_sp, engine='fastparquet')
ff_df = pd.read_parquet(path_ff, engine='fastparquet')

join_df = sp_df.merge(ff_df, on='Date', how='left')

join_df['Excess Return'] = join_df['Monthly Return'] - join_df['RF']

# 5 - itt még kell, hogy symbolon belül csak!

join_df.sort_values('Date')
join_df.loc[join_df['Symbol'] == join_df['Symbol'].shift(-1), 'ex_ret_1'] = join_df['Excess Return'].shift(-1)

# 6

join_df.dropna(subset=['ex_ret_1'], inplace=True)
join_df.dropna(subset=['HML'], inplace=True)

# 7
join_df = join_df.filter(like='AMZN').drop('Symbol', axis=1)

