import FX_Arbitrage as fx
import pandas as pd
import pickle

#load the data
df_list = pickle.load(open( "rates_tables_dictionary.p", "rb" ))
dates = list(df_list.keys())
dfs = list(df_list.values())

#Test df that contains arbitrage
test_data = [[1, 0.639, 0.537, 1.0835, 98.89],
                  [1.564, 1, 0.843, 1.6958, 154.773],
                  [1.856, 1.186, 1, 2.014, 184.122],
                  [0.9223, 0.589, 0.496, 1, 91.263],
                  [0.01011, 0.00645, 0.00543, 0.01095,1]]
cols = ["USD", "EUR", "GBP", "AUD", "JPY"]
test_df = pd.DataFrame(data=test_data, columns=cols, index=cols)


arbs = [fx.FX_Arbitrage(date, df) for date, df in df_list.items()]

for arb in arbs:
    arb.form_lp()

arbs_data = [arb.find_arbitrage() for arb in arbs]