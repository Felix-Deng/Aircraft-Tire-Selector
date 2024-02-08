import time 
import numpy as np 
import matplotlib.pyplot as plt 

from gradients import gradients_opt 
from selector import search_databook 

testing_Lm = np.arange(2000, 72000, 10000) 
total_time = 0 

perf_michelin = [] 
perf_goodyear = [] 
perf_gradients = [] 

time_michelin = [] 
time_goodyear = [] 
time_gradients = [] 

scopes = {
    "Dm": (12, 56), 
    "Wm": (4, 21), 
    "D": (4, 24), 
    "DF": (5, 33), 
    "PR": (4, 38)
}

for Lm in testing_Lm: 
    # Test Michelin 
    st = time.time() 
    tire = search_databook(Lm, source='michelin')
    time_michelin.append(time.time() - st)
    if tire: 
        perf_michelin.append(tire.inflation_medium_mass())
    else: 
        perf_michelin.append(None)
    # Test Goodyear 
    st = time.time() 
    tire = search_databook(Lm, source='goodyear')
    time_goodyear.append(time.time() - st)
    if tire: 
        perf_goodyear.append(tire.inflation_medium_mass())
    else: 
        perf_goodyear.append(None)
    # Test gradients 
    temp_time = [] 
    temp_perf = [] 
    for _ in range(3): 
        st = time.time() 
        tire = gradients_opt(Lm, 0, scopes=scopes) 
        temp_time.append(time.time() - st)
        temp_perf.append(tire.inflation_medium_mass())
    time_gradients.append(np.mean(temp_time))
    perf_gradients.append(np.mean(temp_perf))

# Plotting 
_, ax = plt.subplots()
ax.scatter(testing_Lm, perf_michelin, marker='o', label='Michelin')
ax.scatter(testing_Lm, perf_goodyear, marker='^', label='Goodyear')
ax.scatter(testing_Lm, perf_gradients, marker='x', label='Gradients Method')
ax.set_xlabel("Desired Loading Capability [lbs]")
ax.set_ylabel("Mass of Tire Inflation Medium [kg]")
plt.legend() 
plt.tight_layout() 
plt.show() 
