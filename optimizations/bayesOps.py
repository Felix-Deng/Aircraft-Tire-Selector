"""
The Bayesian optimization (BayesOps) method models the design space with 
Gaussian process regression. Acquisition functions are chosen to 
query additional points of the objective function, creating a better 
modelling to converge towards the objective. 

BayesOps assumes the objective function is expensive to evaluate 
and does not require expensive gradient evaluation. 

Reference: 
[1] Frazier, P. I. (2018). A Tutorial on Bayesian Optimization. 
    http://arxiv.org/abs/1807.02811
[2] Nogueira, F. (2014). Bayesian Optimization: Open source constrained 
    global optimization tool for Python. 
    https://github.com/fmfn/BayesianOptimization 
"""
from typing import Dict, Tuple, Optional
from bayes_opt import BayesianOptimization, UtilityFunction
from _models import Tire
    

def bayes_opt(
    req_Lm: float, speed_index: float, scope: Dict[str, Tuple[float, float]], 
    n_iter: int = 100, util_kind: str = 'ucb', 
    util_kappa: float = 2.576, util_xi: float = 0, 
    util_kappa_decay: float = 1.0, util_kappa_decay_delay: float = 0.0
) -> Optional[Tire]: 
    """Use the Bayesian optimization method to search for an optimized aircraft 
    tire design given scope and utility function hyperparameters. 

    Args:
        req_Lm (float): the minimum required load capacity 
        speed_index (float): the speed index of the target aircraft design 
        scope (Dict[str, Tuple[float, float]]): the domain of all design variables 
            Dict[name_of_variable, Tuple[min_value, max_value]]
        n_iter (int, optional): number of iterations. Defaults to 100.
        util_kind (str, optional): utility function {"ucb", "ei", "poi}. 
            Defaults to 'ucb'.
        util_kappa (float, optional): exploitation (0.1) --> exploration (10). 
            (for ucb only) Defaults to 2.576.
        util_xi (float, optional): exploitation (1e-4) --> exploration (0.1). 
            (for ei and poi only) Defaults to 0.
        util_kappa_decay (float, optional): kappa is multiplied by this factor every iteration. 
            Defaults to 1.0.
        util_kappa_decay_delay (float, optional): number of iterations that must have passed before 
            applying the decay to kappa. Defaults to 0.0.

    Returns:
        Optional[Tire]: the optimized tire design 
    """
    
    def objective_func(Dm, Wm, D, DF, PR) -> float: 
        """Defines the objective function for Bayesian optimization. 

        Returns:
            float: -1 * tire mass (in kg) if all constraints satisfied; return -1e10 otherwise. 
        """
        asp = (Dm - D)/2/Wm
        # Declare constraints 
        if Dm <= DF or DF <= D or asp < 0.5 or asp > 1: 
            return -1e10
        tire = Tire(PR=PR, Dm=Dm, Wm=Wm, D=D, DF=DF)
        if tire.max_load_capacity() < req_Lm: 
            return -1e10
        # True objectives 
        return -tire.inflation_medium_mass() 
    
    acquisition = UtilityFunction(
        kind=util_kind, kappa=util_kappa, xi=util_xi, 
        kappa_decay=util_kappa_decay, kappa_decay_delay=util_kappa_decay_delay
    )
    optimizer = BayesianOptimization(
        f=objective_func, pbounds=scope, verbose=0
    )
    
    # Optimization iteration 
    for i in range(n_iter): 
        next_pt = optimizer.suggest(acquisition)
        target = objective_func(**next_pt)
        try: 
            optimizer.register(params=next_pt, target=target)
        except: 
            pass 
    opt_tire = optimizer.max['params']
    tire = Tire(
        D=opt_tire['D'], DF=opt_tire['DF'], Dm=opt_tire['Dm'], 
        PR=opt_tire['PR'], Wm=opt_tire['Wm']
    )
    
    if tire.max_load_capacity() >= req_Lm: 
        return tire 
    else: 
        return None 


if __name__ == "__main__": 
    scope = {
        "Dm": (12, 56), 
        "Wm": (4, 21), 
        "D": (4, 24), 
        "DF": (5, 33), 
        "PR": (4, 38)
    }

    tire = bayes_opt(
        36000, 0, scope, util_kind='ucb', util_kappa=8, 
        util_kappa_decay=0.95, util_kappa_decay_delay=50
    )
    print(tire)
    
