import csv 
import numpy as np 
import time 

import os 
import sys 
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from models import Tire

# Define generation range 
RANGE_Dm = np.arange(12, 56, 0.5)
RANGE_Wm = np.concatenate((np.arange(4, 10, 0.25), np.arange(10, 21, 0.5)))
RANGE_D = np.arange(4, 24, 1)
RANGE_DF = np.arange(5, 33, 0.25)
RANGE_PR = np.arange(4, 38, 1)

"""Constraints: 
(C1). 4.5 ≤ Dm - DF ≤ 32
(C2). 1 ≤ DF - D ≤ 4.5
(C3). 0.5 ≤ aspect ratio ≤ 1
    aspect ratio = (Dm - D)/2/Wm
"""

# Synthetic design options generation 
data = [
    ["Dm", "Wm", "D", "DF", "PR", "AR", "Lm", "Mass"]
] 

st = time.time() 
for Dm in RANGE_Dm: 
    for DF in RANGE_DF[(4.5 <= Dm - RANGE_DF) & (Dm - RANGE_DF <= 32)]: # (C1)
        for D in RANGE_D[(1 <= DF - RANGE_D) & (DF - RANGE_D <= 4.5)]: # (C2)
            for Wm in RANGE_Wm[(0.5 <= (Dm - D)/2/RANGE_Wm) & ((Dm - D)/2/RANGE_Wm <= 1)]: # (C3)
                for PR in RANGE_PR: 
                    tire = Tire(PR=PR, DoMax=Dm, DoMin=Dm, WMax=Wm, WMin=Wm, RD=D, DF=DF)
                    data.append([
                        Dm, Wm, D, DF, PR, (Dm - D)/2/Wm, 
                        tire.max_load_capacity(), 
                        tire.inflation_medium_mass()
                    ])
et = time.time() 
print("Elapsed time:", et - st, "sec")
print("Number of tires generated:", len(data)-1)

# Save data 
with open('synthetic_data/synthetic_data.csv', 'w') as csvfile: 
    csv_writer = csv.writer(csvfile)
    for row in data: 
        csv_writer.writerow(row)
    