import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from models import Tire 
from selector import search_databook 
from optimizations.randSearch import rs_discrete, rs_continuous
from optimizations.bayesOps import bayes_opt
from optimizations.gradients import gradients_opt

"""
For every function: 

opt_tire = func(req_Lm, speed_index, scope, ...)
"""

scope = {
    "Dm": (12, 56), 
    "Wm": (4, 21), 
    "D": (4, 24), 
    "DF": (5, 33), 
    "PR": (4, 38)
}