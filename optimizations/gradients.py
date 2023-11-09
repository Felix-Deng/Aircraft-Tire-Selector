"""
The gradients-based optimization method utilizes structural multidisciplinary 
design optimization (MDO) framework to optimize the continuous design space. 
Specifically, the openMDAO framework [1], developed by NASA, is utilized in this script. 

[1] Gray, J. S., Hwang, J. T., Martins, J. R. R. A., Moore, K. T., & Naylor, B. A. (2019). 
    OpenMDAO: an open-source framework for multidisciplinary design, analysis, and optimization. 
    Structural and Multidisciplinary Optimization, 59(4), 1075–1104. 
    https://doi.org/10.1007/s00158-019-02211-z
"""

from typing import Dict, Tuple, Optional
import numpy as np 
from scipy.stats import linregress
import openmdao.api as om
import matplotlib.pyplot as plt 
from _models import Tire


def _gradients_opt(
    req_Lm: float, speed_index: float, scopes: Dict[str, Tuple[float, float]], 
    optimizer: str='SLSQP', reports=False
) -> Optional[Tire]: 
    """Use the openMDAO framework to perform gradients-based optimization to search 
    for an optimized aircraft tire design given scopes and solver types. 

    Args:
        req_Lm (float): the minimum required load capacity 
        speed_index (float): the speed index of the target aircraft design 
        scopes (Dict[str, Tuple[float, float]]): the domain of all design variables 
            Dict[name_of_variable, Tuple[min_value, max_value]]
        optimizer (str, optional): optimizer type for om.ScipyOptimizeDriver. Defaults to 'SLSQP'. 
        reports (bool, optional): should reports be auto generated? Defaults to False.

    Returns:
        Optional[Tire]: the optimized tire design 
    """
    init_val = {} # take average for initialized values 
    for key, item in scopes.items(): 
        init_val[key] = (item[0] + item[1]) / 2
    
    class LoadCapacity(om.ExplicitComponent): 
        """The explicit MDA component that defines the discipline 
        (correlation of all optimizing variables) for optimization. 
        """
        def setup(self): 
            self.add_input('Dm', val=init_val['Dm'])
            self.add_input('Wm', val=init_val['Wm'])
            self.add_input('D', val=init_val['D'])
            self.add_input('DF', val=init_val['DF'])
            self.add_input('PR', val=init_val['PR'])
            self.add_output('Lm')
        
        def setup_partials(self):
            self.declare_partials('*', '*', method='fd')
        
        def compute(self, inputs, outputs):
            Dm = inputs['Dm']
            Wm = inputs['Wm']
            D = inputs['D']
            DF = inputs['DF']
            PR = inputs['PR']
            
            tire = Tire(PR=PR, Dm=Dm, Wm=Wm, RD=D, DF=DF)
            outputs['Lm'] = tire.max_load_capacity(exact=True)

    class GasMass(om.ExplicitComponent): 
        """The explicite MDA component that defines the objective 
        for optimization. 
        """
        def setup(self): 
            self.add_input('Dm', val=init_val['Dm'])
            self.add_input('Wm', val=init_val['Wm'])
            self.add_input('D', val=init_val['D'])
            self.add_input('DF', val=init_val['DF'])
            self.add_input('PR', val=init_val['PR'])
            self.add_output('mass')
        
        def setup_partials(self):
            self.declare_partials('*', '*', method='fd')
        
        def compute(self, inputs, outputs):
            Dm = inputs['Dm']
            Wm = inputs['Wm']
            D = inputs['D']
            DF = inputs['DF']
            PR = inputs['PR']
            
            tire = Tire(PR=PR, Dm=Dm, Wm=Wm, RD=D, DF=DF)
            outputs['mass'] = tire.inflation_medium_mass()
            

    class TireMDA(om.Group): 
        """The MDA group that connects all disciplines, 
        objectives, and constraints for optimization. 
        """
        def setup(self):
            cycle = self.add_subsystem('cycle', om.Group())
            cycle.add_subsystem('d', LoadCapacity())
            
            cycle.nonlinear_solver = om.NonlinearBlockGS()
            cycle.linear_solver = om.ScipyKrylov()
            
            self.add_subsystem('obj_cmp', GasMass())
            
            self.add_subsystem(
                'con_cmp1', om.ExecComp('con1 = mass')
            )
            self.add_subsystem(
                'con_cmp2', om.ExecComp('con2 = Dm - DF', Dm=init_val['Dm'], DF=init_val['DF'])
            )
            self.add_subsystem(
                'con_cmp3', om.ExecComp('con3 = DF - D', DF=init_val['DF'], D=init_val['D'])
            )
            self.add_subsystem(
                'con_cmp4', om.ExecComp(
                    'con4 = (Dm - D) / 2 / Wm', 
                    Dm=init_val['Dm'], D=init_val['D'], Wm=init_val['Wm']
                )
            ) # aspect ratio 
            
            
        def configure(self):
            self.cycle.promotes('d', inputs=['Dm', 'Wm', 'D', 'DF', 'PR'], outputs=['Lm'])
            self.promotes('cycle', any=['*'])
            
            self.promotes('obj_cmp', any=['Dm', 'Wm', 'D', 'DF', 'PR', 'mass'])
            self.promotes('con_cmp1', any=['con1', 'mass'])
            self.promotes('con_cmp2', any=['con2', 'Dm', 'DF'])
            self.promotes('con_cmp3', any=['con3', 'DF', 'D'])
            self.promotes('con_cmp4', any=['con4', 'Dm', 'D', 'Wm'])
            
            self.add_design_var('Dm', lower=scopes['Dm'][0], upper=scopes['Dm'][1])
            self.add_design_var('Wm', lower=scopes['Wm'][0], upper=scopes['Wm'][1])
            self.add_design_var('D', lower=scopes['D'][0], upper=scopes['D'][1])
            self.add_design_var('DF', lower=scopes['DF'][0], upper=scopes['DF'][1])
            self.add_design_var('PR', lower=scopes['PR'][0], upper=scopes['PR'][1])
            
            self.add_objective("mass")
            self.add_constraint('con1', lower=0.0001)
            self.add_constraint('con2', lower=0.0001)
            self.add_constraint('con3', lower=0.0001)
            self.add_constraint('con4', lower=0.5, upper=1.0) # TRA standard
    
    prob = om.Problem(reports=reports) 
    prob.model = TireMDA()
    prob.driver = om.ScipyOptimizeDriver(optimizer=optimizer) 
    
    prob.model.add_constraint('Lm', lower=req_Lm) 
    prob.model.approx_totals() 
    
    prob.setup() 
    prob.set_solver_print(level=-1)
    fail_fag = prob.run_driver() 
    
    if fail_fag: 
        return None 
    
    tire = Tire(
        Dm=prob.get_val('Dm')[0], 
        Wm=prob.get_val('Wm')[0], 
        RD=prob.get_val('D')[0], 
        DF=prob.get_val('DF')[0], 
        PR=prob.get_val('PR')[0]
    )
    return tire 

def gradients_opt(
    req_Lm: float, speed_index: float, scopes: Dict[str, Tuple[float, float]], 
    optimizer: str='SLSQP', reports=False
) -> Tire: 
    """Use the openMDAO framework to perform gradients-based optimization to search 
    for an optimized aircraft tire design given scopes and solver types. 

    Args:
        req_Lm (float): the minimum required load capacity 
        speed_index (float): the speed index of the target aircraft design 
        scopes (Dict[str, Tuple[float, float]]): the domain of all design variables 
            Dict[name_of_variable, Tuple[min_value, max_value]]
        optimizer (str, optional): optimizer type for om.ScipyOptimizeDriver. Defaults to 'SLSQP'. 
        reports (bool, optional): should reports be auto generated? Defaults to False.

    Returns:
        Tire: the optimized tire design 
    """
    tire = None 
    counter = 0 
    while not tire: 
        counter += 1
        if counter > 1: 
            print("openMDAO optimization failed to return a valid tire design. Starting attempt number {} ...".format(counter))
        tire = _gradients_opt(req_Lm, speed_index, scopes, optimizer, reports)
        req_Lm += 1
    return tire 
        
    
def eval_gradients_opt(
    scopes: Dict[str, Tuple[float, float]], 
    num=30, range_l=1000, range_u=76001, show_plot=False, num_summary=True
) -> float:
    """Test the performance (load capacity of the tires) of the optimization 
    setup by comparing the expected performance to the performance of the 
    optimized model. 

    Args:
        scopes (Dict[str, Tuple[float, float]]): the domain of all design variables 
            Dict[name_of_variable, Tuple[min_value, max_value]]
        num (int, optional): number of data points to be tested. Defaults to 30.
        range_u (int, optional): upper bound of the testing range of the required 
            load capacity. Defaults to 1000.
        range_l (int, optional): lower bound of the testing range of the required 
            load capacity. Defaults to 76001.
        show_plot (bool, optional): show the comparison plot. Defaults to False.
        num_summary (bool, optional): print out a summary of number of models optimized. 
            Defaults to True. 

    Returns:
        float: the standard error of the linear regression fitted for the comparison. 
    """
    expected = np.arange(range_l, range_u, (range_u - range_l) // num)
    evaluated = [] # keep track of values of successful optimizations 
    optimized = [] 
    
    for Lm in expected: 
        tire = gradients_opt(Lm, 0, scopes)
        evaluated.append(Lm)
        optimized.append(tire.max_load_capacity(exact=False))
    
    if show_plot: 
        plt.scatter(evaluated, optimized)
        plt.plot(expected, expected, ls='--')
        plt.xlabel("Required Lm")
        plt.ylabel("Optimized Lm")
        plt.tight_layout() 
        plt.show() 
    
    if num_summary: 
        print(f'''{'*' * 30}
Number of models optimized: 
    Total: {len(expected)}
    successful: {len(optimized)}
    Success rate: {len(optimized) / len(expected)}
{'*' * 30}''')
    
    return linregress(evaluated, optimized).stderr
    

if __name__ == "__main__":     
    scopes = {
        "Dm": (12, 56), 
        "Wm": (4, 21), 
        "D": (4, 24), 
        "DF": (5, 33), 
        "PR": (4, 38)
    }
    # tire = gradients_opt(36000, 0, scopes)
    tire = gradients_opt(61000, 0, scopes)
    print(tire)
    
    # print(
    #     "Standard Error between required and optimized Lm:", 
    #     eval_gradients_opt(scopes, show_plot=True)
    # )
    