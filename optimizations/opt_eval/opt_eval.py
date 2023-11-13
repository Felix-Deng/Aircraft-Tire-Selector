# %% 
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from randSearch import rs_discrete, rs_continuous
from bayesOps import bayesOps_opt
from gradients import gradients_opt
from genAlg import ga_opt 
from selector import search_databook

import time 
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
Lm_testing_range = np.arange(1000, 76000, 10000)

# Optimization results: List[Tuple[Lm, mass]]
res_manu = [] 
res_rs_disc = [] 
res_rs_cont = [] 
res_bayes = [] 
res_gradients = [] 
res_ga = [] 

start_time = time.time()
for i, req_Lm in enumerate(Lm_testing_range): 
    enum_time = time.time() 
    
    tire = search_databook(req_Lm)
    res_manu.append(tire)
    
    tire = rs_discrete(req_Lm, 0, scope_disc, 1)
    res_rs_disc.append(tire)
    
    tire = rs_continuous(req_Lm, 0, scope_cont, 1)
    res_rs_cont.append(tire)
    
    tire = bayesOps_opt(
        req_Lm, 0, scope_cont, init_points=10, n_iter=100, util_kind='ucb', util_kappa=8, 
        util_kappa_decay=0.95, util_kappa_decay_delay=50
    )
    res_bayes.append(tire)
    
    tire = gradients_opt(req_Lm, 0, scope_cont)
    res_gradients.append(tire)
    
    tire = ga_opt(req_Lm, 0, scope_cont)
    res_ga.append(tire)
    
    print("{}\nAnalysis {}/{} completed \t req_Lm = {}\nLm Elapsed Time: {} s \t Total Elapsed Time: {} s\n{}".format(
        "*"*50, i+1, len(Lm_testing_range), round(req_Lm, 2), 
        round(time.time() - enum_time, 2), round(time.time() - start_time, 2), "*"*50
    ))

# %% Plot req_Lm vs. opt_Lm 
fig, ax = plt.subplots()
ax.plot(Lm_testing_range, Lm_testing_range, '--', label='Reference')
ax.scatter(Lm_testing_range, [res.max_load_capacity(exact=True) for res in res_manu], label='Manufacturer Databook')
ax.scatter(Lm_testing_range, [res.max_load_capacity(exact=True) for res in res_rs_disc], label='Random Search (Discrete)')
ax.scatter(Lm_testing_range, [res.max_load_capacity(exact=True) for res in res_rs_cont], label='Random Search (Continuous)')
ax.scatter(Lm_testing_range, [res.max_load_capacity(exact=True) for res in res_bayes], label='Bayesian Optimization')
ax.scatter(Lm_testing_range, [res.max_load_capacity(exact=True) for res in res_gradients], label='Gradients-Based Optimization')
ax.scatter(Lm_testing_range, [res.max_load_capacity(exact=True) for res in res_ga], label='Gentic Algorithm')
ax.legend() 
ax.set_xlabel("Required Lm (lbs)")
ax.set_ylabel("Optimized Lm (lbs)")
plt.tight_layout() 
plt.show() 

# %% Plot req_Lm vs. opt_mass 
fig, ax = plt.subplots()
ax.scatter(Lm_testing_range, [res.inflation_medium_mass() for res in res_manu], label='Manufacturer Databook')
ax.scatter(Lm_testing_range, [res.inflation_medium_mass() for res in res_rs_disc], label='Random Search (Discrete)')
ax.scatter(Lm_testing_range, [res.inflation_medium_mass() for res in res_rs_cont], label='Random Search (Continuous)')
ax.scatter(Lm_testing_range, [res.inflation_medium_mass() for res in res_bayes], label='Bayesian Optimization')
ax.scatter(Lm_testing_range, [res.inflation_medium_mass() for res in res_gradients], label='Gradients-Based Optimization')
ax.scatter(Lm_testing_range, [res.inflation_medium_mass() for res in res_ga], label='Genetic Algorithm')
ax.legend() 
ax.set_xlabel("Required Lm (lbs)")
ax.set_ylabel("Tire Mass (kg)")
plt.tight_layout() 
plt.show() 
# %% Plot req_Lm vs. asp_ratio
fig, ax = plt.subplots() 
ax.scatter(Lm_testing_range, [res.aspect_ratio() for res in res_manu], label='Manufacturer Databook')
ax.scatter(Lm_testing_range, [res.aspect_ratio() for res in res_rs_disc], label='Random Search (Discrete)')
ax.scatter(Lm_testing_range, [res.aspect_ratio() for res in res_rs_cont], label='Random Search (Continuous)')
ax.scatter(Lm_testing_range, [res.aspect_ratio() for res in res_bayes], label='Bayesian Optimization')
ax.scatter(Lm_testing_range, [res.aspect_ratio() for res in res_gradients], label='Gradients-Based Optimization')
ax.scatter(Lm_testing_range, [res.aspect_ratio() for res in res_ga], label='Genetic Algorithm')
ax.legend() 
ax.set_xlabel("Required Lm (lbs)")
ax.set_ylabel("Aspect Ratio")
plt.tight_layout() 
plt.show() 

# %%
