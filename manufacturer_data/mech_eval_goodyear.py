import re
import csv 
import numpy as np 
from scipy import constants 
import matplotlib.pyplot as plt 
import matplotlib.ticker as mtick 

from _models import Tire


# Retrieve given tire data 
with open("manufacturer_data/goodyear_bias.csv") as data_csv: 
    csv_reader = csv.reader(data_csv)
    # next(csv_reader)  # skip header row
    calc_result = [] 
    for i, row in enumerate(csv_reader): 
        if i == 0: 
            calc_result.append(
                row + [
                    'Rounded Calc Lm', 'Exact Calc Lm', 
                    'Rounded Lm Relative Difference', 
                    'Absolute Relative Difference', 'Comment'
                ] + [
                    "Fiber (rho={})".format(i) for i in np.linspace(0.85, 0.95, 5)
                ]
            )
            continue 
        """ Column index: [
            'M', 'N', 'PR', 'TT/TL', 'SI', 'Lm', 'IP', 'RL', 'BL', 'TD', 'PRT', 'WGT', 
            'DoMax', 'DoMin', 'WMax', 'WMin', 'DsMax', 'WsMax', 'LR_RL', 'LR_BL', 'AR', 
            'WS', 'A', 'RD', 'FH', 'G', 'AM', 'QS'
        ]
        """
        # Data clean up 
        float_dim = ['0' if x == '' else x for x in row] # Replace empty elements with '0'
        if 'K' in float_dim[4]: # Check SI (could be in kt or mph or LS)
            float_dim[4] = float(float_dim[4][:-1]) * constants.knot / constants.mph
            
        # Convert All elements to floats
        for i, dim in enumerate(float_dim): 
            try: 
                float_dim[i] = float(dim)
            except: 
                pass 
        
        # With every row of data, create a new Tire object to calculate maximum load capacity (Lm) 
        if (float_dim[5] != 0) and (float_dim[12] != 0) and (float_dim[13] != 0):
            tire = Tire(
                M=float_dim[0], N=float_dim[1], D=float_dim[23], PR=float_dim[2], SI=float_dim[4], 
                Lm=float_dim[5], IP=float_dim[6], BL=float_dim[8], DoMax=float_dim[12], DoMin=float_dim[13], WMax=float_dim[14], 
                WMin=float_dim[15], DsMax=float_dim[16], WsMax=float_dim[17], AR=float_dim[20], LR_RL=float_dim[18], LR_BL=float_dim[19], 
                A=float_dim[22], RD=float_dim[23], FH=float_dim[24], G=float_dim[25], QS=row[-1]
            )
        
            databook_Lm = tire.Lm
            rounded_Lm = tire.max_load_capacity()
            exact_Lm = round(tire.max_load_capacity(exact=True), 2)
            diff_ratio = round((rounded_Lm - databook_Lm) / databook_Lm, 2)
            abs_diff_ratio = abs(diff_ratio)
            if (tire.Lr <= 1.5)|(tire.Lr >= 5):
                comment = 'Lr = {}, Lm to be comfirmed'.format(tire.Lr)
            else:
                comment = ''
            fiber = [tire.walter_fiber_count(prho=i) for i in np.linspace(0.85, 0.95, 5)]
            calc_result.append(row + [rounded_Lm, exact_Lm, diff_ratio, abs_diff_ratio, comment] + fiber)
        else:
            calc_result.append(row + [0, 0, 'N/A', 'N/A', 'No enough info'] + [0] * 5)

# Save the calculated Lm to a new CSV to compare with given manufacturer values 
with open("manufacturer_data/mech_eval_goodyear.csv", "w") as out_csv: 
    csv_writer = csv.writer(out_csv)
    csv_writer.writerows(calc_result)