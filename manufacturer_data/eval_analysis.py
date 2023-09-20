import pandas as pd 
import statsmodels.api as sm 
from scipy.stats import linregress
import matplotlib.pyplot as plt 

df = pd.read_csv("manufacturer_data/eval_results.csv", date_format=float)
print("Average Error:", df['Rounded Lm Relative Difference'].mean())

# Multiple linear regression 
x = df[[
    'M', 'N', 'D', 'PR', 'Lm', 'IP', 'BL', 'DoMax', 'DoMin', 
    'WMax', 'WMin', 'DsMax', 'WsMax', 'AR', 'LR_RL', 'LR_BL', 'A', 'RD', 
    'FH', 'G', 'DF'
]]
X = sm.add_constant(x)
y = df['Rounded Lm Relative Difference']
model = sm.OLS(y, X, missing="drop")
results = model.fit() 
print(results.summary())

# Sort by scale of error 
sorted_df = df.sort_values(by=["Absolute Relative Difference"], ascending=False)
sorted_df.to_csv("manufacturer_data/sorted_eval.csv")

# Print standard error between manufacturer Lm and calculated Lm (rounded)
print()
err_df = df[['Lm', 'Rounded Calc Lm']].dropna()
print(f"Included tires: {len(err_df)}/{len(df)}")
print("Standard error:", linregress(err_df['Lm'], err_df['Rounded Calc Lm']).stderr)

# Plot relationship between individual parameter 
param = "Lm"
plt.scatter(df[param], df['Rounded Lm Relative Difference'])
plt.xlabel(param)
plt.ylabel("Relative Error")
plt.tight_layout() 
plt.show() 
