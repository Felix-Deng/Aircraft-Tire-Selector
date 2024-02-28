import re
import csv
import copy 
import time 
from typing import Optional

import numpy as np 
from scipy import constants 

from _models import Tire

def search_databook(Lm_des: float, speed_index_des=0.0, max_pressure=float('inf'), source='michelin') -> Optional[Tire]:
    """Given the desired loading capacity, find the corresponding tire specifications 
    from the Michelin Tire Databook. 

    Args:
        Lm_des (float): required tire loading capability in lbs. 
        speed_index_des (float, optional): designed speed rating for the aircraft in mph. Defaults to 0.0.
        max_pressure (float, optional): maximum pressure that the tire can be inflated to. Defaults to inf. 
        source (str, optional): source of manufacturer databook from {'michelin', 'goodyear'}. 
            Defaults to 'michelin'. 

    Returns:
        Optional[Tire]: recommended lightest tire based on manufacturer databook. 
    """
    best_tire = None 
    lowest_mass = float('inf') 
    
    if source == 'michelin': 
        with open("manufacturer_data/michelin_bias.csv") as data_csv: 
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
                    (not speed_index_des or not manu_dim[4] or manu_dim[4] >= speed_index_des) and # check if speed index meet requirement (if any)
                    manu_dim[6] <= max_pressure # check if inflation pressure exceeds maximum 
                ):
                    tire = Tire(
                        D=manu_dim[2], PR=manu_dim[3], SI=manu_dim[4], Lm=manu_dim[5], 
                        DoMax=manu_dim[8], DoMin=manu_dim[9], WMax=manu_dim[10], 
                        WMin=manu_dim[11], RD=manu_dim[18], FH=manu_dim[19], DF=manu_dim[21], 
                        IP=manu_dim[6] 
                    )
                    if tire.IP or tire.inflation_pressure() <= max_pressure: # account for tires with inflation pressure missing 
                        curr_mass = tire.inflation_medium_mass()
                        # Check if better than current best 
                        if curr_mass < lowest_mass: 
                            lowest_mass = curr_mass 
                            best_tire = copy.deepcopy(tire) 
    elif source == 'goodyear': 
        with open("manufacturer_data/goodyear_bias.csv") as data_csv: 
            csv_reader = csv.reader(data_csv)
            next(csv_reader)  # skip header row
            
            for row in csv_reader:
                # Data clean up 
                manu_dim = ['0' if x == '' else x for x in row] # replace empty elements with '0'
                if 'K' in manu_dim[4]: # Check SI (could be in kt or mph or LS)
                    manu_dim[4] = float(manu_dim[4][:-1]) * constants.knot / constants.mph
                
                # Convert all elements to floats
                for i, dim in enumerate(manu_dim): 
                    try: 
                        manu_dim[i] = float(dim)
                    except: 
                        pass 
                
                # Check fitness for consideration 
                if (
                    (manu_dim[5] and manu_dim[12]) and # required design parameters present 
                    manu_dim[5] >= Lm_des and # check if Lm meet requirement 
                    (not speed_index_des or not manu_dim[4] or manu_dim[4] >= speed_index_des) and # check if speed index meet requirement (if any)
                    manu_dim[6] <= max_pressure # check if inflation pressure exceeds maximum 
                ):
                    tire = Tire(
                        D=manu_dim[23], PR=manu_dim[2], SI=manu_dim[4], Lm=manu_dim[5], 
                        DoMax=manu_dim[12], DoMin=manu_dim[13], WMax=manu_dim[14], 
                        WMin=manu_dim[15], RD=manu_dim[23], FH=manu_dim[24], 
                        IP=manu_dim[6], WGT=manu_dim[11]
                    )
                    if tire.IP or tire.inflation_pressure() <= max_pressure: # account for tires with inflation pressure missing 
                        curr_mass = tire.mass
                        # Check if better than current best 
                        if curr_mass < lowest_mass: 
                            lowest_mass = curr_mass 
                            best_tire = copy.deepcopy(tire) 
    else: 
        raise ValueError("Unsupported source, please choose from {'michelin', 'goodyear'}.") 
    
    if not best_tire: 
        print("No suitable tire design options can be found from the manufacturer databook.")
    return best_tire

def eval_selector(Lm_testing_range=(2000, 72000), Lm_step=10000, iter_per_Lm=3, source='michelin') -> float: 
    """
    Args:
        Lm_testing_range (tuple, optional): lower and upper bound of Lm for testing. 
            Defaults to (2000, 72000).
        Lm_step (int, optional): step size for Lm to be tested. Defaults to 10000.
        iter_per_Lm (int, optional): number of tests for every Lm tested. 
            Defaults to 3.
        source (str, optional): source of manufacturer databook from {'michelin', 'goodyear'}. 
            Defaults to 'michelin'. 

    Returns:
        float: average time required for one tire selection. 
    """
    testing_Lm = np.arange(Lm_testing_range[0], Lm_testing_range[1] + Lm_step, Lm_step)
    total_time = 0
    for Lm in testing_Lm: 
        for _ in range(iter_per_Lm): 
            st = time.time() 
            _ = search_databook(Lm, source=source)
            total_time += time.time() - st 
    return total_time / len(testing_Lm) / 3


if __name__ == "__main__": 
    print(search_databook(30000, source='goodyear'))
    # print(eval_selector(source='michelin'))
