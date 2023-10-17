"""
The random search (RS) method starts with a random value assignment to 
each variable, it then iteratively moves to better neighboring positions 
(as defined by the objective function) in the search space. Iterations 
repeat for a pre-defined number of times, runtime, or fitness. 
"""

import time 
import copy 
import numpy as np 
from typing import Optional, Dict, List
from _models import Tire 


def is_geo_valid(dim: List[float], req_Lm: float) -> bool: 
    """Given a tire design, evaluate if the design is geometrically valid based on 
    established constraints, and evaluate if the estimated loading capacity meets 
    the required loading. 

    Args:
        geo_dim (List[float]): geometric dimensions of the tire 
            [PR, Dm, Wm, D, DF]
        req_Lm (float): required minimum aircraft loading 

    Returns:
        bool: if the geometry is valid for the aircraft 
    """
    PR, Dm, Wm, D, DF = dim
    asp = (Dm - D)/2/Wm
    if Dm <= DF or DF <= D or asp < 0.5 or asp > 1: 
        return False 
    tire = Tire(PR=PR, Dm=Dm, Wm=Wm, RD=D, DF=DF)
    if tire.load_supporting_capability() < req_Lm: 
        return False 
    return True 

def rs_discrete(
    req_Lm: float, scope: Dict[str, np.ndarray], step_size: int, 
    iter=10000, runtime=15*60, fitness=1e-6
) -> Optional[Tire]: 
    """Use random search (RS) to search for an optimized tire design 
    in the discrete design space. 

    Args:
        req_Lm (float): minimum required loading capability 
        scope (Dict[str, np.ndarray]): the domain of all design variables 
            Dict[name_of_variable, array_of_all_available_values]
        step_size (int): radius of the hypersphere, in number of array index 
        iter (int, optional): stopping criterion in number of iterations. Defaults to 10000.
        runtime (_type_, optional): stopping criterion in runtime length (sec). 
            Defaults to 15*60.
        fitness (_type_, optional): stopping criterion in optimization fitness 
            (% improvement relative to previous iteration). Defaults to 1e-6.

    Returns:
        Optional[Tire]: the optimized tire design located within stopping criteria. 
    """
    start_time = time.time()
    
    while True: 
        PR = scope['PR'][np.random.randint(0, len(scope['PR']))]
        Dm = scope['Dm'][np.random.randint(0, len(scope['Dm']))]
        Wm = scope['Wm'][np.random.randint(0, len(scope['Wm']))]
        D = scope['D'][np.random.randint(0, len(scope['D']))]
        DF = scope['DF'][np.random.randint(0, len(scope['DF']))]
        geo_dim = [PR, Dm, Wm, D, DF]
        if is_geo_valid(geo_dim, req_Lm): 
            break 
        if time.time() - start_time >= runtime: 
            print("Random Search failed to start with a valid initial random value assignment. Please try again ...")
            return None 
    
    prev_tire = Tire(PR=geo_dim[0], Dm=geo_dim[1], Wm=geo_dim[2], RD=geo_dim[3], DF=geo_dim[4])
    
    for i in range(iter): 
        # Construct the hypersphere with radius step_size        
        tires = [
            # List[Tire, new_geo_dim]
            [
                Tire(PR=scope['PR'][np.where(scope['PR'], geo_dim[0])[0][0] + step_size], Dm=geo_dim[1], Wm=geo_dim[2], RD=geo_dim[3], DF=geo_dim[4]), 
                [scope['PR'][np.where(scope['PR'], geo_dim[0])[0][0] + step_size], geo_dim[1], geo_dim[2], geo_dim[3], geo_dim[4]]
            ], 
            [
                Tire(PR=scope['PR'][np.where(scope['PR'], geo_dim[0])[0][0] - step_size], Dm=geo_dim[1], Wm=geo_dim[2], RD=geo_dim[3], DF=geo_dim[4]), 
                [scope['PR'][np.where(scope['PR'], geo_dim[0])[0][0] - step_size], geo_dim[1], geo_dim[2], geo_dim[3], geo_dim[4]]
            ], 
            [
                Tire(PR=geo_dim[0], Dm=scope['Dm'][np.where(scope['Dm'], geo_dim[1])[0][0] + step_size], Wm=geo_dim[2], RD=geo_dim[3], DF=geo_dim[4]),
                [geo_dim[0], scope['Dm'][np.where(scope['Dm'], geo_dim[1])[0][0] + step_size], geo_dim[2], geo_dim[3], geo_dim[4]]
            ], 
            [
                Tire(PR=geo_dim[0], Dm=scope['Dm'][np.where(scope['Dm'], geo_dim[1])[0][0] - step_size], Wm=geo_dim[2], RD=geo_dim[3], DF=geo_dim[4]),
                [geo_dim[0], scope['Dm'][np.where(scope['Dm'], geo_dim[1])[0][0] - step_size], geo_dim[2], geo_dim[3], geo_dim[4]]
            ], 
            [
                Tire(PR=geo_dim[0], Dm=geo_dim[1], Wm=scope['Wm'][np.where(scope['Wm'], geo_dim[2])[0][0] + step_size], RD=geo_dim[3], DF=geo_dim[4]),
                [geo_dim[0], geo_dim[1], scope['Wm'][np.where(scope['Wm'], geo_dim[2])[0][0] + step_size], geo_dim[3], geo_dim[4]]
            ], 
            [
                Tire(PR=geo_dim[0], Dm=geo_dim[1], Wm=scope['Wm'][np.where(scope['Wm'], geo_dim[2])[0][0] - step_size], RD=geo_dim[3], DF=geo_dim[4]),
                [geo_dim[0], geo_dim[1], scope['Wm'][np.where(scope['Wm'], geo_dim[2])[0][0] - step_size], geo_dim[3], geo_dim[4]]
            ], 
            [
                Tire(PR=geo_dim[0], Dm=geo_dim[1], Wm=geo_dim[2], RD=scope['RD'][np.where(scope['RD'], geo_dim[3])[0][0] + step_size], DF=geo_dim[4]),
                [geo_dim[0], geo_dim[1], geo_dim[2], scope['RD'][np.where(scope['RD'], geo_dim[3])[0][0] + step_size], geo_dim[4]]
            ], 
            [
                Tire(PR=geo_dim[0], Dm=geo_dim[1], Wm=geo_dim[2], RD=scope['RD'][np.where(scope['RD'], geo_dim[3])[0][0] - step_size], DF=geo_dim[4]),
                [geo_dim[0], geo_dim[1], geo_dim[2], scope['RD'][np.where(scope['RD'], geo_dim[3])[0][0] - step_size], geo_dim[4]]
            ], 
            [
                Tire(PR=geo_dim[0], Dm=geo_dim[1], Wm=geo_dim[2], RD=geo_dim[3], DF=scope['DF'][np.where(scope['DF'], geo_dim[4])[0][0] + step_size]),
                [geo_dim[0], geo_dim[1], geo_dim[2], geo_dim[3], scope['DF'][np.where(scope['DF'], geo_dim[4])[0][0] + step_size]]
            ], 
            [
                Tire(PR=geo_dim[0], Dm=geo_dim[1], Wm=geo_dim[2], RD=geo_dim[3], DF=scope['DF'][np.where(scope['DF'], geo_dim[4])[0][0] - step_size]),
                [geo_dim[0], geo_dim[1], geo_dim[2], geo_dim[3], scope['DF'][np.where(scope['DF'], geo_dim[4])[0][0] - step_size]]
            ]
        ] 
        
        next_tire = sorted(
            [t for t in tires if is_geo_valid(t[1], req_Lm)], 
            key=lambda x:x[0].inflation_medium_mass()
        )[0]
        if not next_tire: 
            print("Random Search failed to find a feasible next location in the hypersphere after {} iterations.\nThe (sub)optimized design from the last iteration is returned.\nPlease consider a different step size and try again ...".format(i))
            return prev_tire
        geo_dim = copy.deepcopy(next_tire[1])
        next_tire = next_tire[0]
        
        if (
            prev_tire.inflation_medium_mass() - next_tire.inflation_medium_mass()
        ) / prev_mass.inflation_medium_mass() <= fitness or time.time() - start_time >= runtime: 
            print("{} optimization iterations carried out.".format(i))
            return next_tire 
        else: 
            prev_mass =  next_tire
    
    print("{} optimization iterations carried out.".format(i))
    return next_tire 
    
    
if __name__ == "__main__": 
    np.random.seed(80)
    # Define generation range 
    RANGE_Dm = np.arange(12, 56, 0.5)
    RANGE_Wm = np.concatenate((np.arange(4, 10, 0.25), np.arange(10, 21, 0.5)))
    RANGE_D = np.arange(4, 24, 1)
    RANGE_DF = np.arange(5, 33, 0.25)
    RANGE_PR = np.arange(4, 38, 1)
    scope = {
        "Dm": RANGE_Dm, 
        "Wm": RANGE_Wm, 
        "D": RANGE_D, 
        "DF": RANGE_DF, 
        "PR": RANGE_PR
    }
    
    tire = rs_discrete(36000, scope, 1, runtime=5 * 60)
    print("Dm: ", tire.Dm)
    print("Wm: ", tire.Wm)
    print("D: ", tire.D)
    print("DF: ", tire.DF)
    print("PR: ", tire.PR)
    print("Lm: ", tire.load_supporting_capability())