"""
The random search (RS) method starts with a random value assignment to 
each variable, it then iteratively moves to better neighboring positions 
(as defined by the objective function) in the search space. Iterations 
repeat for a pre-defined number of times, runtime, or fitness. 
"""

import time 
import copy 
import numpy as np 
import itertools
from typing import Optional, Union, Dict, List, Tuple
from _models import Tire 


def is_geo_valid(dim: List[float], req_Lm: float) -> Union[Tire, bool]: 
    """Given a tire design, evaluate if the design is geometrically valid based on 
    established constraints, and evaluate if the estimated loading capacity meets 
    the required loading. 

    Args:
        geo_dim (List[float]): geometric dimensions of the tire 
            [PR, Dm, Wm, D, DF]
        req_Lm (float): required minimum aircraft loading 

    Returns:
        Union[Tire, bool]: return the Tire object if the geometry is valid for 
            the aircraft; return False otherwise 
    """
    PR, Dm, Wm, D, DF = dim
    asp = (Dm - D)/2/Wm
    if Dm <= DF or DF <= D or asp < 0.5 or asp > 1: 
        return False 
    tire = Tire(PR=PR, Dm=Dm, Wm=Wm, D=D, DF=DF)
    if tire.max_load_capacity() < req_Lm: 
        return False 
    return tire 

def rs_discrete(
    req_Lm: float, speed_index: float, scopes: Dict[str, np.ndarray], step_size: int, 
    iter=1000, runtime=15*60, fitness=1e-3, init_dim=[] 
) -> Optional[Tire]: 
    """Use random search (RS) to search for an optimized tire design 
    in the discrete design space. 

    Args:
        req_Lm (float): minimum required loading capability 
        speed_index (float): the speed index of the target aircraft design 
        scopes (Dict[str, np.ndarray]): the domain of all design variables 
            Dict[name_of_variable, array_of_all_available_values]
        step_size (int): radius of the hypersphere, in number of array index 
        iter (int, optional): stopping criterion in number of iterations. Defaults to 10000.
        runtime (float, optional): stopping criterion in runtime length (sec). 
            Defaults to 15*60.
        fitness (float, optional): stopping criterion in optimization fitness 
            (% improvement relative to previous iteration). Defaults to 1e-6.
        init_dim (List[float], optional): user-specified initial dimensions 
            [PR, Dm, Wm, D, DF] to be used instead of randomly initiating. 
            Defaults to []

    Returns:
        Optional[Tire]: the optimized tire design located within stopping criteria. 
    """
    start_time = time.time()
    design_var = ['PR', 'Dm', 'Wm', 'D', 'DF'] 
    
    # Locate an initial position 
    if init_dim: 
        init_tire = is_geo_valid(init_dim, req_Lm)
        if not init_tire: 
            print("Provided initial dimension is not valid geometrically or cannot support the required loading.\nRandom value assignment is being carried out ...")
            random_init = True 
        else: 
            random_init = False 
    else: 
        random_init = True 
    if random_init: 
        while True: 
            geo_dim = [
                scopes[var][np.random.randint(0, len(scopes[var]))] 
                for var in design_var
            ]
            init_tire = is_geo_valid(geo_dim, req_Lm) 
            if init_tire: 
                break 
            if time.time() - start_time >= runtime: 
                print("Random Search failed to start with a valid initial random value assignment. Please try again ...")
                return None 
    
    # Search for the next optimal position 
    move_options = [p for p in itertools.product([-1, 0, 1], repeat=len(design_var))]
    curr_best_tire = init_tire
    for i in range(iter): 
        curr_best_dim = curr_best_tire.get_key_dim()
        iter_best_tire = copy.deepcopy(curr_best_tire)
        # Construct the hypersphere with radius step_size 
        for move in move_options: 
            temp_dim = [] 
            valid_move = True 
            for ind, var in enumerate(design_var): 
                scope_ind = np.where(scopes[var] == curr_best_dim[ind])[0][0]
                move_ind = scope_ind + move[ind] * step_size
                # Check if the new move is going out of the variable's scope 
                if 0 <= move_ind < len(scopes[var]): 
                    temp_dim.append(scopes[var][move_ind])
                else: 
                    valid_move = False 
                    break 
            if valid_move: 
                temp_tire = is_geo_valid(temp_dim, req_Lm)
                # Check if this is the best in the hypersphere so far 
                if temp_tire and temp_tire.inflation_medium_mass() < iter_best_tire.inflation_medium_mass(): 
                    iter_best_tire = copy.deepcopy(temp_tire)
        
        if iter_best_tire == curr_best_tire: 
            print("Random Search failed to find a feasible next location in the hypersphere after {} iterations.\nThe (sub)optimized design from the last iteration is returned.\nPlease consider a different step size and try again ...".format(i))
            return curr_best_tire
        else: 
            if (
                curr_best_tire.inflation_medium_mass() - iter_best_tire.inflation_medium_mass()
            ) / curr_best_tire.inflation_medium_mass() <= fitness or time.time() - start_time >= runtime: 
                print("{} optimization iterations carried out.".format(i))
                return iter_best_tire
            else: 
                curr_best_tire = copy.deepcopy(iter_best_tire)
    
    print("{} optimization iterations carried out.".format(i))
    return curr_best_tire 
    
def rs_continuous(
    req_Lm: float, speed_index: float, scopes: Dict[str, Tuple[float, float]], step_size: float, 
    iter=1000, runtime=15*60, fitness=1e-3, init_dim=[] 
) -> Optional[Tire]: 
    """Use random search (RS) to search for an optimized tire design 
    in the continuous design space. 

    Args:
        req_Lm (float): minimum required loading capability 
        speed_index (float): the speed index of the target aircraft design 
        scopes (Dict[str, Tuple[float, float]]): the domain of all design variables 
            Dict[name_of_variable, Tuple[min_value, max_value]]
        step_size (float): radius of the hypersphere, in float step increment
        iter (int, optional): stopping criterion in number of iterations. Defaults to 10000.
        runtime (float, optional): stopping criterion in runtime length (sec). 
            Defaults to 15*60.
        fitness (float, optional): stopping criterion in optimization fitness 
            (% improvement relative to previous iteration). Defaults to 1e-6.
        init_dim (List[float], optional): user-specified initial dimensions 
            [PR, Dm, Wm, D, DF] to be used instead of randomly initiating. 
            Defaults to []

    Returns:
        Optional[Tire]: the optimized tire design located within stopping criteria. 
    """
    start_time = time.time()
    design_var = ['PR', 'Dm', 'Wm', 'D', 'DF'] 
    
    # Locate an initial position 
    if init_dim: 
        init_tire = is_geo_valid(init_dim, req_Lm)
        if not init_tire: 
            print("Provided initial dimension is not valid geometrically or cannot support the required loading.\nRandom value assignment is being carried out ...")
            random_init = True 
        else: 
            random_init = False 
    else: 
        random_init = True 
    if random_init: 
        while True: 
            geo_dim = [
                np.random.rand() * (scopes[var][1] - scopes[var][0]) + scopes[var][0]
                for var in design_var
            ]
            init_tire = is_geo_valid(geo_dim, req_Lm) 
            if init_tire: 
                break 
            if time.time() - start_time >= runtime: 
                print("Random Search failed to start with a valid initial random value assignment. Please try again ...")
                return None 
    
    # Search for the next optimal position 
    move_options = [p for p in itertools.product([-1, 0, 1], repeat=len(design_var))]
    curr_best_tire = init_tire
    for i in range(iter): 
        curr_best_dim = curr_best_tire.get_key_dim()
        iter_best_tire = copy.deepcopy(curr_best_tire)
        # Construct the hypersphere with radius step_size 
        for move in move_options: 
            temp_dim = [] 
            valid_move = True 
            for ind, var in enumerate(design_var): 
                move_val = curr_best_dim[ind] + move[ind] * step_size
                # Check if the new move is going out of the variable's scope 
                if scopes[var][0] <= move_val < scopes[var][1]: 
                    temp_dim.append(move_val)
                else: 
                    valid_move = False 
                    break 
            if valid_move: 
                temp_tire = is_geo_valid(temp_dim, req_Lm)
                # Check if this is the best in the hypersphere so far 
                if temp_tire and temp_tire.inflation_medium_mass() < iter_best_tire.inflation_medium_mass(): 
                    iter_best_tire = copy.deepcopy(temp_tire)
        
        if iter_best_tire == curr_best_tire: 
            print("Random Search failed to find a feasible next location in the hypersphere after {} iterations.\nThe (sub)optimized design from the last iteration is returned.\nPlease consider a different step size and try again ...".format(i))
            return curr_best_tire
        else: 
            if (
                curr_best_tire.inflation_medium_mass() - iter_best_tire.inflation_medium_mass()
            ) / curr_best_tire.inflation_medium_mass() <= fitness or time.time() - start_time >= runtime: 
                print("{} optimization iterations carried out.".format(i))
                return iter_best_tire
            else: 
                curr_best_tire = copy.deepcopy(iter_best_tire)
    
    print("{} optimization iterations carried out.".format(i))
    return curr_best_tire 

    
if __name__ == "__main__": 
    # np.random.seed(80)
    
    # Test discrete design space 
    scopes = {
        "Dm": np.arange(12, 56, 0.5), 
        "Wm": np.concatenate((np.arange(4, 10, 0.25), np.arange(10, 21, 0.5))), 
        "D": np.arange(4, 24, 1), 
        "DF": np.arange(5, 33, 0.25), 
        "PR": np.arange(4, 38, 1)
    }
    tire = rs_discrete(36000, 0, scopes, 1, runtime=10 * 60)
    # tire = rs_discrete(36000, scope, 1, runtime=10 * 60, init_dim=[28, 43, 16, 20, 23.5])
    print("Dm: ", tire.Dm)
    print("Wm: ", tire.Wm)
    print("D: ", tire.D)
    print("DF: ", tire.DF)
    print("PR: ", tire.PR)
    print("Lm: ", tire.max_load_capacity())
    print("Mass_tire: ", tire.inflation_medium_mass())
    
    # Test continuous design space 
    scopes = {
        "Dm": (12, 56), 
        "Wm": (4, 21), 
        "D": (4, 24), 
        "DF": (5, 33), 
        "PR": (4, 38)
    }
    tire = rs_continuous(36000, 0, scopes, 1, runtime=10 * 60)
    # tire = rs_continuous(36000, scope, 1, runtime=10 * 60, init_dim=[28, 43, 16, 20, 23.5])
    print("Dm: ", tire.Dm)
    print("Wm: ", tire.Wm)
    print("D: ", tire.D)
    print("DF: ", tire.DF)
    print("PR: ", tire.PR)
    print("Lm: ", tire.max_load_capacity())
    print("Mass_tire: ", tire.inflation_medium_mass())