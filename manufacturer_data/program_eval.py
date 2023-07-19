import csv 
import matplotlib.pyplot as plt 
import sys
import os
import re

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from models import Tire


# Retrieve given tire data 
with open("manufacturer_data/tire_data.csv") as data_csv: 
    csv_reader = csv.reader(data_csv)
    next(csv_reader)  # skip header row
    calc_result = [['Databook Lm', 'Rounded Calc Lm', 'Exact Calc Lm', 'Rounded Lm Difference Percent', 'Comment']] 
    for row in csv_reader: 
        """Column index: [
            'Pre', 'M', 'N', 'D', 'PR', 'SI', 'Lm', 'IP', 'BL', 
            'DoMax', 'DoMin', 'WMax', 'WMin', 'DsMax', 'WsMax', 
            'AR', 'LR_RL', 'LR_BL', 'A', 'RD', 'FH', 'G', 'DF', 'QS'
        ]
        """
        # With every row of data, create a new Tire object to 
        # calculate maximum load capacity (Lm) 
        ##### Write your code below #####
        
        #Replace empty elements with '0'
        float_dim = ['0' if x == '' else x for x in row[1:-1]]
        
        #Check SI (could be in kt or mph or LS)
        if 'kt' in float_dim[4].lower():
            #format can be 195kt, 195 kt , 195 Kt ,
            float_dim[4] = re.sub('[A-Za-z ]+', '', float_dim[4])
            #One Knot = 1.151 mile per hour
            float_dim[4] = float(float_dim[4].split()[0]) * 1.151
        #Using 1 to represent LS 
        elif 'ls' in float_dim[4].lower():
            float_dim[4] = '1'
       
        #Convert All elements to floats
        float_dim = [float(dim) for dim in float_dim]
        #print(float_dim)
        if (float_dim[5] != 0) and (float_dim[8] != 0) and (float_dim[9] != 0):
            tire = Tire(Pre=row[0], M=float_dim[0], N=float_dim[1], D=float_dim[2], PR=float_dim[3], SI=float_dim[4], 
            Lm=float_dim[5], IP=float_dim[6], BL=float_dim[7], DoMax=float_dim[8], DoMin=float_dim[9], WMax=float_dim[10], 
            WMin=float_dim[11], DsMax=float_dim[12], WsMax=float_dim[13], AR=float_dim[14], LR_RL=float_dim[15], LR_BL=float_dim[16], 
            A=float_dim[17], RD=float_dim[18], FH=float_dim[19], G=float_dim[20], DF=float_dim[21], QS=row[-1])
        
            Databook_Lm = tire.Lm
            Rounded_Lm = tire.max_load_capacity()
            Exact_Lm = round(tire.max_load_capacity(exact=True), 2)
            diff_ratio = round(abs(tire.Lm-tire.max_load_capacity())/(tire.Lm)*100)
            if (tire.Lr <= 1.5)|(tire.Lr >= 5):
                comment = 'Lr = {}, Lm to be comfirmed'.format(tire.Lr)
            else:
                comment = ''
            calc_result.append([Databook_Lm, Rounded_Lm, Exact_Lm, diff_ratio, comment])
        else:
            calc_result.append([float_dim[5], 0, 0, 'No enough info'])


# Save the calculated Lm to a new CSV to compare with given 
# manufacturer values 
with open("manufacturer_data/eval_results.csv", "w") as out_csv: 
    csv_writer = csv.writer(out_csv)
    ##### Write your code below #####
    csv_writer.writerows(calc_result)
    
# Show a distribution plot of the percentage errors between 
# calculation results and manufacturer data
difference = [row[3] for row in calc_result[1:]]
difference = [element for element in difference if isinstance(element, int)]
plt.hist(difference, bins = 10, range = (0, 60))
#plt.tight_layout() 
plt.xlabel('Difference in Percentage range 0 to 60')
plt.show() 
#plt.savefig("eval_results.png")