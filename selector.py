import re
import csv
import copy 
from typing import Optional

import numpy as np 
from scipy import constants 

from models import Tire

def search_databook(Lm_des: float, speed_index_des=0.0) -> Optional[Tire]:
    """Given the desired loading capacity, find the corresponding tire specifications 
    from the Michelin Tire Databook. 

    Args:
        Lm_des (float): required tire loading capability in lbs. 
        speed_index_des (float, optional): designed speed rating for the aircraft in mph. Defaults to 0.0.

    Returns:
        Optional[Tire]: recommended lightest tire based on manufacturer databook. 
    """
    best_tire = None 
    lowest_mass = float('inf') 
    
    with open("manufacturer_data/tire_data.csv") as data_csv: 
        csv_reader = csv.reader(data_csv)
        next(csv_reader)  # skip header row
        
        for row in csv_reader:
            # Data clean up 
            manu_dim = ['0' if x == '' else x for x in row[1:-1]] # replace empty elements with '0'
            if 'kt' in manu_dim[4].lower(): # convert kt to mph 
                manu_dim[4] = float(re.sub('[A-Za-z ]+', '', manu_dim[4]).split()[0]) * constants.knot / constants.mph
            elif 'ls' in manu_dim[4].lower(): # assign 1 mph for LS ratings 
                manu_dim[4] = '1'
            manu_dim = [float(dim) for dim in manu_dim] # convert all elements to floats

            # Check fitness for consideration 
            if (
                (manu_dim[5] and manu_dim[9]) and # required design parameters present 
                manu_dim[5] >= Lm_des and # check if Lm meet requirement 
                (not speed_index_des or not manu_dim[4] or manu_dim[4] >= speed_index_des) # check if speed index meet requirement (if any)
            ):
                tire = Tire(
                    D=manu_dim[2], PR=manu_dim[3], SI=manu_dim[4], Lm=manu_dim[5], 
                    DoMax=manu_dim[8], DoMin=manu_dim[9], WMax=manu_dim[10], 
                    WMin=manu_dim[11], RD=manu_dim[18], FH=manu_dim[19], DF=manu_dim[21]
                )
                curr_mass = tire.inflation_medium_mass()
                # Check if better than current best 
                if curr_mass < lowest_mass: 
                    lowest_mass = curr_mass 
                    best_tire = copy.deepcopy(tire) 
    
    if not best_tire: 
        print("No suitable tire design options can be found from the manufacturer databook.")
    return best_tire

print(search_databook(30000))
