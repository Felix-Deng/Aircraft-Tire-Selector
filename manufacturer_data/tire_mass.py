import csv 
import numpy as np 
import pandas as pd 
import seaborn as sns 
from scipy import constants, stats 
import matplotlib.pyplot as plt 
from _models import Tire 


manu_Lm = [] 
model_Lm = [] 
manu_IP = [] 
model_IP = [] 

tire_weight = [] 
gas_weight = [] 

with open("manufacturer_data/goodyear_bias.csv") as data_csv: 
    csv_reader = csv.reader(data_csv)
    next(csv_reader)
    
    for row in csv_reader: 
        if "K" in row[4]: 
            c_SI = float(row[4][:-1]) * constants.knot / constants.mph 
        else: 
            c_SI = float(row[4])
        
        tire = Tire(
            M=float(row[0]), N=float(row[1]), PR=float(row[2]), SI=c_SI, 
            Lm=float(row[5]), IP=float(row[6]), BL=float(row[8]), 
            DoMax=float(row[12]), DoMin=float(row[13]), WMax=float(row[14]), 
            WMin=float(row[15]), DsMax=float(row[16]), WsMax=float(row[17]), 
            LR_RL=float(row[18]), LR_BL=float(row[19]), AR=float(row[20]),
            A=float(row[22]), RD=float(row[23]), FH=float(row[24]), G=float(row[25]) 
        )
        
        manu_Lm.append(float(row[5]))
        model_Lm.append(tire.max_load_capacity())
        manu_IP.append(float(row[6]))
        model_IP.append(tire.inflation_pressure())
        tire_weight.append(float(row[11]) * constants.lb)
        gas_weight.append(tire.inflation_medium_mass())
        
print(np.mean([model_Lm[i] - item for i, item in enumerate(manu_Lm)]))
print(np.mean([model_IP[i] - item for i, item in enumerate(manu_IP)])) 


df = pd.DataFrame({
    "tire": tire_weight, 
    "gas": gas_weight
})

sns.regplot(data=df, x='tire', y='gas', ci=90, color='red')
plt.xlabel("Overall Mass of Tire [kg]")
plt.ylabel("Mass of Tire Inflation Medium [kg]")
plt.tight_layout() 
plt.show() 

lin_res = stats.linregress(tire_weight, gas_weight)
print(stats.linregress(gas_weight, tire_weight))