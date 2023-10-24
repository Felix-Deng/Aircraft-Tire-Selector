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
from bayes_opt import BayesianOptimization, UtilityFunction
from _models import Tire

LM_DESIRED = 36000

def objective_func (Dm, Wm, D, DF, PR): 
    asp = (Dm - D)/2/Wm
    # Declare constraints 
    if Dm <= DF or DF <= D or asp < 0.5 or asp > 1: 
        return -100000
    tire = Tire(PR=PR, Dm=Dm, Wm=Wm, D=D, DF=DF)
    if tire.max_load_capacity() < LM_DESIRED: 
        return -100000
    # True objectives 
    return -tire.inflation_medium_mass() 
    

scope = {
    "Dm": [12, 56], 
    "Wm": [4, 21], 
    "D": [4, 24], 
    "DF": [5, 33], 
    "PR": [4, 38]
}

# Acquisition function 
# kappa: exploitation (0.1) --> exploration (10)
# xi: exploitation (1e-4) --> exploration (0.1)
acquisition = UtilityFunction(kind='ucb', kappa=8, kappa_decay=0.95, kappa_decay_delay=50)
# acquisition = UtilityFunction(kind='ei', xi=0.07)
# acquisition = UtilityFunction(kind='poi', xi=0.07)

# Bayesian optimization setup 
optimizer = BayesianOptimization(
    f=objective_func, 
    pbounds=scope, 
    verbose=2  # 1 prints only when max observed, 0 for silent 
)

# Optimization iteration 
# optimizer.maximize(init_points=5, n_iter=100)
for i in range(100): 
    next_pt = optimizer.suggest(acquisition)
    target = objective_func(**next_pt)
    try: 
        optimizer.register(params=next_pt, target=target)
    except: 
        pass 

opt_tire = optimizer.max["params"]
print("Best result: {}".format(opt_tire))
tire = Tire(
    D=opt_tire['D'], DF=opt_tire['DF'], Dm=opt_tire['Dm'], 
    PR=opt_tire['PR'], Wm=opt_tire['Wm']
)
print("Required Lm: {}\nOptimized tire Lm: {}".format(
    LM_DESIRED, tire.max_load_capacity()
))
print("Optimized tire mass: {}".format(tire.inflation_medium_mass()))
