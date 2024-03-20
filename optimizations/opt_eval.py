import time 
import numpy as np 
import matplotlib.pyplot as plt 
from scipy import stats 
from gradients import gradients_opt 
from selector import search_databook 

testing_Lm = np.linspace(2000, 72000, 10)

Lm_michelin = [] 
Lm_goodyear = []
Lm_gradients = [] 

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
    tire = search_databook(Lm, max_pressure=400, source='michelin')
    time_michelin.append(time.time() - st)
    if tire: 
        Lm_michelin.append(Lm)
        perf_michelin.append(tire.estimated_tire_mass())
    # Test Goodyear 
    st = time.time() 
    tire = search_databook(Lm, max_pressure=400, source='goodyear')
    time_goodyear.append(time.time() - st)
    if tire: 
        Lm_goodyear.append(Lm)
        perf_goodyear.append(tire.mass)
    # Test gradients 
    st = time.time() 
    tire = gradients_opt(Lm, 0, max_inflation_pressure=400, scopes=scopes) 
    if tire: 
        time_gradients.append(time.time() - st)
        perf_gradients.append(tire.estimated_tire_mass())
        Lm_gradients.append(Lm)

# Line of best fit 
lin_res = stats.linregress(Lm_michelin, perf_michelin)
michelin_m, michelin_b = lin_res.slope, lin_res.intercept
print("Michelin:", lin_res)
lin_res = stats.linregress(Lm_goodyear, perf_goodyear)
goodyear_m, good_year_b = lin_res.slope, lin_res.intercept
print("Goodyear:", lin_res)
lin_res = stats.linregress(Lm_gradients, perf_gradients)
gradients_m, gradients_b = lin_res.slope, lin_res.intercept
print("openMDAO:", lin_res)

# Plotting mass performance 
plt.rcParams.update({
    'font.size': 28 
})
s = 200 # marker size 

_, ax = plt.subplots(figsize=(16, 10))
ax.scatter(Lm_michelin, perf_michelin, marker='o', s=s, label='Michelin', color='grey')
ax.scatter(Lm_goodyear, perf_goodyear, marker='^', s=s, label='Goodyear', color='grey')
ax.scatter(Lm_gradients, perf_gradients, marker='x', s=s, label='Developed Framework', color='red')

x = np.array([Lm_michelin[0], Lm_michelin[-1]]) 
ax.plot(x, michelin_m * x + michelin_b, ls='--', color='grey', lw=3)
x = np.array([Lm_goodyear[0], Lm_goodyear[-1]]) 
ax.plot(x, goodyear_m * x + good_year_b, ls='--', color='grey', lw=3)
x = np.array([Lm_gradients[0], Lm_gradients[-1]]) 
ax.plot(x, gradients_m * x + gradients_b, ls='--', color='red', lw=3)

ax.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
ax.set_xlabel("Desired Loading Capability [lbs]")
ax.set_ylabel("Estimated Tire Mass [kg]")
plt.legend() 
plt.tight_layout() 
plt.show() 

# Plotting computational time 
_, ax = plt.subplots()
ax.scatter(Lm_gradients, time_gradients, marker='x')
ax.hlines(max(time_gradients), xmin=ax.get_xlim()[0], xmax=ax.get_xlim()[1], ls='--', color='black')
ax.text(0, max(time_gradients)+0.001, str(round(max(time_gradients), 4)))
ax.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
ax.set_xlabel("Desired Loading Capability [lbs]")
ax.set_ylabel("Expected Computation Time [sec]")
plt.tight_layout() 
plt.show() 
