"""
The gradients-based optimization method utilizes structural multidisciplinary 
design optimization (MDO) framework to optimize the continuous design space. 
Specifically, the openMDAO framework [1], developed by NASA, is utilized in this script. 

[1] Gray, J. S., Hwang, J. T., Martins, J. R. R. A., Moore, K. T., & Naylor, B. A. (2019). 
    OpenMDAO: an open-source framework for multidisciplinary design, analysis, and optimization. 
    Structural and Multidisciplinary Optimization, 59(4), 1075–1104. 
    https://doi.org/10.1007/s00158-019-02211-z
"""

import time 
from typing import Dict, Tuple, Optional, Union 

import numpy as np 
from scipy.stats import linregress
import matplotlib.pyplot as plt 
import openmdao.api as om

from _models import Tire
from selector import search_databook 


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
    scopes: Dict[str, Tuple[float, float]], optimizer: str='SLSQP', 
    Lm_testing_range=(2000, 72000), Lm_step=10000, iter_per_Lm=3, show_plot=True
) -> Union[float, float]:
    """Test the performance (load capacity of the tires) of the optimization 
    setup by comparing the expected performance to the performance of the 
    optimized model. 

    Args:
        scopes (Dict[str, Tuple[float, float]]): the domain of all design variables 
            Dict[name_of_variable, Tuple[min_value, max_value]]
        optimizer (str, optional): optimizer type for om.ScipyOptimizeDriver. Defaults to 'SLSQP'. 
        Lm_testing_range (tuple, optional): lower and upper bound of Lm for testing. 
            Defaults to (2000, 72000).
        Lm_step (int, optional): step size for Lm to be tested. Defaults to 10000.
        iter_per_Lm (int, optional): number of tests for every Lm tested. 
            Defaults to 3.
        show_plot (bool, optional): show the comparison plot. Defaults to True.
        
    Returns:
        Union[float, float]: optimality and efficiency of the testing pop_size. 
    """
    testing_Lm = np.arange(Lm_testing_range[0], Lm_testing_range[1] + Lm_step, Lm_step)
    opt_Lm, opt_mass, opt_AR, time_used = [], [], [], []
    
    for Lm in testing_Lm: 
        temp_Lm, temp_mass, temp_AR, temp_time = [], [], [], [] 
        ref_tire = search_databook(Lm)
        for _ in range(iter_per_Lm): 
            st = time.time() 
            tire = gradients_opt(Lm, 0, scopes, optimizer)
            temp_time.append(time.time() - st)
            temp_Lm.append(tire.max_load_capacity(exact=True) - Lm)
            temp_mass.append(ref_tire.inflation_medium_mass() - tire.inflation_medium_mass())
            temp_AR.append(tire.aspect_ratio())
        opt_Lm.append(temp_Lm)
        opt_mass.append(temp_mass)
        opt_AR.append(temp_AR)
        time_used.append(temp_time)
    
    optimality = sum([np.mean(item) for item in opt_mass])
    efficiency = np.mean([np.mean(item) for item in time_used])
    # print("Optimality:", optimality)
    # print("Efficiency:", efficiency)
    
    # Optimization results plot 
    if show_plot: 
        _, axs = plt.subplots(3, 1, sharex='all', figsize=(10, 10))
        axs[0].boxplot(opt_Lm)
        axs[0].set_ylabel("Lm(opt) - Lm(des) [lbs]")
        axs[1].boxplot(opt_mass)
        axs[1].set_ylabel("Tire mass [kg]")
        axs[2].boxplot(opt_AR)
        axs[2].set_ylabel("Aspect ratio")
        
        axs[2].set_xticks(np.arange(1, len(testing_Lm) + 1))
        axs[2].set_xticklabels(testing_Lm, rotation=90)
        axs[2].set_xlabel("Lm(des) [lbs]")
        axs[0].set_title("Optimization Evaluation for Genetic Algorithm (GA)")
        plt.tight_layout() 
        plt.show() 

        # Performance results plot 
        _, ax = plt.subplots()
        ax.boxplot(time_used)
        ax.set_ylabel("Time used per optimization [sec]")
        ax.set_xticks(np.arange(1, len(testing_Lm) + 1))
        ax.set_xticklabels(testing_Lm, rotation=90)
        ax.set_xlabel("Lm(des) [lbs]")
        ax.set_title("Performance Evaluation for Genetic Algorithm (GA)")
        plt.tight_layout() 
        plt.show() 
    
    return optimality, efficiency
    

if __name__ == "__main__":     
    scopes = {
        "Dm": (12, 56), 
        "Wm": (4, 21), 
        "D": (4, 24), 
        "DF": (5, 33), 
        "PR": (4, 38)
    }
    tire = gradients_opt(36000, 0, scopes)
    print(tire)
    
    # opt, eff = eval_gradients_opt(scopes, optimizer='SLSQP')
    # print("Optimality: {}, efficiency: {}".format(opt, eff))
    
    