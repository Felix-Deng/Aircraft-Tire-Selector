import pandas as pd
usecols = ["Fiber (rho=0.85)","Fiber (rho=0.875)","Fiber (rho=0.8999999999999999)","Fiber (rho=0.9249999999999999)","Fiber (rho=0.95)"]
#michelin_data = pd.read_csv("manufacturer_data/mech_eval_michelin.csv",usecols=usecols)
good_year_data = pd.read_csv("manufacturer_data/mech_eval_goodyear.csv",usecols=usecols)
#michelin_data = michelin_data.loc[~(michelin_data == 0).all(axis=1)]
good_year_data = good_year_data.loc[~(good_year_data == 0).all(axis=1)]
print(good_year_data.describe())
