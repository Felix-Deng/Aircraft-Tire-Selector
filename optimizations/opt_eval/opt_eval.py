import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from randSearch import rs_discrete, rs_continuous
from bayesOps import bayes_opt
from gradients import gradients_opt
from selector import search_databook 

import numpy as np 
import matplotlib.pyplot as plt 

scope_cont = {
    "Dm": (12, 56), 
    "Wm": (4, 21), 
    "D": (4, 24), 
    "DF": (5, 33), 
    "PR": (4, 38)
}
scope_disc = {
    "Dm": np.arange(12, 56, 0.5), 
    "Wm": np.concatenate((np.arange(4, 10, 0.25), np.arange(10, 21, 0.5))), 
    "D": np.arange(4, 24, 1), 
    "DF": np.arange(5, 33, 0.25), 
    "PR": np.arange(4, 38, 1)
}
Lm_testing_range = np.arange(1000, 76000, 1000)

# Optimization results: List[Tuple[Lm, mass]]
res_rs_disc = [] 
res_rs_cont = [] 
res_bayes = [] 
res_gradients = [] 

for req_Lm in Lm_testing_range: 
    # TODO: Add error handling 
    tire = rs_discrete(req_Lm, 0, scope_disc, 1)
    res_rs_disc.append((tire.max_load_capacity(), tire.inflation_medium_mass()))
    
    tire = rs_continuous(req_Lm, 0, scope_cont, 1)
    res_rs_cont.append((tire.max_load_capacity(), tire.inflation_medium_mass()))
    
    tire = bayes_opt(
        req_Lm, 0, scope_cont, n_iter=200, util_kind='ucb', util_kappa=8, 
        util_kappa_decay=0.95, util_kappa_decay_delay=50
    )
    res_bayes.append((tire.max_load_capacity(), tire.inflation_medium_mass()))
    
    tire = gradients_opt(req_Lm, 0, scope_cont)
    res_gradients.append((tire.max_load_capacity(), tire.inflation_medium_mass()))
    
# Plot req_Lm vs. opt_Lm 
fig, ax = plt.subplots()
ax.scatter(Lm_testing_range, [res[0] for res in res_rs_disc], label='Random Search (Discrete)')
ax.scatter(Lm_testing_range, [res[0] for res in res_rs_cont], label='Random Search (Continuous)')
ax.scatter(Lm_testing_range, [res[0] for res in res_bayes], label='Bayesian Optimization')
ax.scatter(Lm_testing_range, [res[0] for res in res_gradients], label='Gradients-Based Optimization')
ax.legend() 
ax.set_xlabel("Required Lm (lbs)")
ax.set_ylabel("Optimized Lm (lbs)")
plt.tight_layout() 
plt.show() 

# Plot req_Lm vs. opt_mass 
fig, ax = plt.subplots()
ax.scatter(Lm_testing_range, [res[1] for res in res_rs_disc], label='Random Search (Discrete)')
ax.scatter(Lm_testing_range, [res[1] for res in res_rs_cont], label='Random Search (Continuous)')
ax.scatter(Lm_testing_range, [res[1] for res in res_bayes], label='Bayesian Optimization')
ax.scatter(Lm_testing_range, [res[1] for res in res_gradients], label='Gradients-Based Optimization')
ax.legend() 
ax.set_xlabel("Required Lm (lbs)")
ax.set_ylabel("Tire Mass (kg)")
plt.tight_layout() 
plt.show() 