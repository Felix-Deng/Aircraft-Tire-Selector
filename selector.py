import csv
import numpy as np 
from scipy import constants 
import re

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from models import Tire

def find_tiredim(Lm):
    """Given the desired loading capacity, find the corresponding tire specifications from Michelin Tire Databook, 
    and arrange them from lowest mass to highest mass

    Args:
        Lm (float): The required loading capacity
    """
    tire_list = [['Dm', 'Wm', 'D','DF','PR','Gas mass']]
    with open("manufacturer_data/tire_data.csv") as data_csv: 
        csv_reader = csv.reader(data_csv)
        next(csv_reader)  # skip header row
        for i, row in enumerate(csv_reader):
            # Data clean up 
            float_dim = ['0' if x == '' else x for x in row[1:-1]] # Replace empty elements with '0'
            if 'kt' in float_dim[4].lower(): # Check SI (could be in kt or mph or LS)
                float_dim[4] = re.sub('[A-Za-z ]+', '', float_dim[4]) # format can be 195kt, 195 kt , 195 Kt ,
                float_dim[4] = float(float_dim[4].split()[0]) * constants.knot / constants.mph
            elif 'ls' in float_dim[4].lower(): # Using 1 to represent LS 
                float_dim[4] = '1'
            float_dim = [float(dim) for dim in float_dim] # Convert All elements to floats
        
            # With every row of data, create a new Tire object to calculate maximum load capacity (Lm) 
            if (float_dim[5] != 0) and (float_dim[8] != 0) and (float_dim[9] != 0):
                tire = Tire(
                    Pre=row[0].strip(), M=float_dim[0], N=float_dim[1], D=float_dim[2], PR=float_dim[3], SI=float_dim[4], 
                    Lm=float_dim[5], IP=float_dim[6], BL=float_dim[7], DoMax=float_dim[8], DoMin=float_dim[9], WMax=float_dim[10], 
                    WMin=float_dim[11], DsMax=float_dim[12], WsMax=float_dim[13], AR=float_dim[14], LR_RL=float_dim[15], LR_BL=float_dim[16], 
                    A=float_dim[17], RD=float_dim[18], FH=float_dim[19], G=float_dim[20], DF=float_dim[21], QS=row[-1]
                )
        
                databook_Lm = tire.Lm
                gass_mass = tire.inflation_medium_mass()
                #rounded_Lm = tire.max_load_capacity()
                #exact_Lm = round(tire.max_load_capacity(exact=True), 2)
                #diff_ratio = round((rounded_Lm - databook_Lm) / databook_Lm, 2)
                #abs_diff_ratio = abs(diff_ratio)
                if float(Lm) == databook_Lm: #find the column meet the requirement
                    tire_list.append([tire.Dm, tire.Wm, tire.D, tire.DF, tire.PR, gass_mass])
    return tire_list

tire_list = find_tiredim(3000)
print(tire_list)