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
"""
