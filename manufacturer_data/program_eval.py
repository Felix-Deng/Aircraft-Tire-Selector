import re
import csv 
import matplotlib.pyplot as plt 
import matplotlib.ticker as mtick 

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from models import Tire


# Retrieve given tire data 
with open("manufacturer_data/tire_data.csv") as data_csv: 
    csv_reader = csv.reader(data_csv)
    next(csv_reader)  # skip header row
    calc_result = [['Databook Lm', 'Rounded Calc Lm', 'Exact Calc Lm', 'Rounded Lm Relative Difference', 'Comment']] 
    for row in csv_reader: 
        """Column index: [
            'Pre', 'M', 'N', 'D', 'PR', 'SI', 'Lm', 'IP', 'BL', 
            'DoMax', 'DoMin', 'WMax', 'WMin', 'DsMax', 'WsMax', 
            'AR', 'LR_RL', 'LR_BL', 'A', 'RD', 'FH', 'G', 'DF', 'QS'
        ]
        """
        # Data clean up 
        float_dim = ['0' if x == '' else x for x in row[1:-1]] # Replace empty elements with '0'
        if 'kt' in float_dim[4].lower(): # Check SI (could be in kt or mph or LS)
            float_dim[4] = re.sub('[A-Za-z ]+', '', float_dim[4]) # format can be 195kt, 195 kt , 195 Kt ,
            float_dim[4] = float(float_dim[4].split()[0]) * 1.151 # 1 Knot = 1.151 mph
        elif 'ls' in float_dim[4].lower(): # Using 1 to represent LS 
            float_dim[4] = '1'
        float_dim = [float(dim) for dim in float_dim] # Convert All elements to floats
        
        # With every row of data, create a new Tire object to calculate maximum load capacity (Lm) 
        if (float_dim[5] != 0) and (float_dim[8] != 0) and (float_dim[9] != 0):
            tire = Tire(
                Pre=row[0], M=float_dim[0], N=float_dim[1], D=float_dim[2], PR=float_dim[3], SI=float_dim[4], 
                Lm=float_dim[5], IP=float_dim[6], BL=float_dim[7], DoMax=float_dim[8], DoMin=float_dim[9], WMax=float_dim[10], 
                WMin=float_dim[11], DsMax=float_dim[12], WsMax=float_dim[13], AR=float_dim[14], LR_RL=float_dim[15], LR_BL=float_dim[16], 
                A=float_dim[17], RD=float_dim[18], FH=float_dim[19], G=float_dim[20], DF=float_dim[21], QS=row[-1]
            )
        
            databook_Lm = tire.Lm
            rounded_Lm = tire.max_load_capacity()
            exact_Lm = round(tire.max_load_capacity(exact=True), 2)
            diff_ratio = round(abs(databook_Lm - rounded_Lm) / databook_Lm, 2)
            if (tire.Lr <= 1.5)|(tire.Lr >= 5):
                comment = 'Lr = {}, Lm to be comfirmed'.format(tire.Lr)
            else:
                comment = ''
            calc_result.append([databook_Lm, rounded_Lm, exact_Lm, diff_ratio, comment])
        else:
            calc_result.append([float_dim[5], 0, 0, 'N/A', 'No enough info'])


# Save the calculated Lm to a new CSV to compare with given manufacturer values 
with open("manufacturer_data/eval_results.csv", "w") as out_csv: 
    csv_writer = csv.writer(out_csv)
    csv_writer.writerows(calc_result)
    
# Show a distribution plot of the percentage errors between calculation results and manufacturer data
difference = [row[3] for row in calc_result[1:]]
difference = [element * 100 for element in difference if isinstance(element, float)]
# difference = [element * 100 for element in difference if isinstance(element, float) and element <= 0.55] # zoom 
fig, ax = plt.subplots(1, 1)
ax.hist(difference)
ax.set_xlabel('Relative Error of Calculation Results')
ax.set_ylabel('Number of Calculations')
ax.xaxis.set_major_formatter(mtick.PercentFormatter())
plt.tight_layout() 
plt.savefig("manufacturer_data/eval_results.png")
plt.show() 