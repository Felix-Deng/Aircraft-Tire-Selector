from typing import Tuple
import numpy as np 
from scipy.stats import linregress
import openmdao.api as om
import matplotlib.pyplot as plt 
from models import Tire

class LoadCapacity(om.ExplicitComponent): 
    """The explicit MDA component that defines the discipline 
    (correlation of all optimizing variables) for optimization. 
    """
    def setup(self): 
        self.add_input('Dm', val=30)
        self.add_input('Wm', val=10)
        self.add_input('D', val=15)
        self.add_input('DF', val=15)
        self.add_input('PR', val=20)
        self.add_output('Lm')
    
    def setup_partials(self):
        self.declare_partials('*', '*', method='fd')
    
    def compute(self, inputs, outputs):
        Dm = inputs['Dm']
        Wm = inputs['Wm']
        D = inputs['D']
        DF = inputs['DF']
        PR = inputs['PR']
        
        tire = Tire(PR=PR, DoMax=Dm, DoMin=Dm, WMax=Wm, WMin=Wm, RD=D, DF=DF)
        outputs['Lm'] = tire.max_load_capacity(exact=True)


class GasMass(om.ExplicitComponent): 
    """The explicite MDA component that defines the objective 
    for optimization. 
    """
    def setup(self): 
        self.add_input('Dm', val=30)
        self.add_input('Wm', val=10)
        self.add_input('D', val=15)
        self.add_input('DF', val=15)
        self.add_input('PR', val=20)
        self.add_output('mass')
    
    def setup_partials(self):
        self.declare_partials('*', '*', method='fd')
    
    def compute(self, inputs, outputs):
        Dm = inputs['Dm']
        Wm = inputs['Wm']
        D = inputs['D']
        DF = inputs['DF']
        PR = inputs['PR']
        
        tire = Tire(PR=PR, DoMax=Dm, DoMin=Dm, WMax=Wm, WMin=Wm, RD=D, DF=DF)
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
            'con_cmp2', om.ExecComp('con2 = Dm - DF', Dm=30, DF=15)
        )
        self.add_subsystem(
            'con_cmp3', om.ExecComp('con3 = DF - D', DF=15, D=15)
        )
        self.add_subsystem(
            'con_cmp4', om.ExecComp(
                'con4 = (Dm - D) / 2 / Wm', Dm=30, D=15, Wm=10
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
        
        self.add_design_var('Dm', lower=12, upper=57)
        self.add_design_var('Wm', lower=4, upper=21)
        self.add_design_var('D', lower=4, upper=28)
        self.add_design_var('DF', lower=5.1, upper=33)
        self.add_design_var('PR', lower=4, upper=38)
        
        self.add_objective("mass")
        self.add_constraint('con1', lower=0.0001)
        self.add_constraint('con2', lower=0.0001)
        self.add_constraint('con3', lower=0.0001)
        self.add_constraint('con4', lower=0.25, upper=1.0) # TRA standard

def optimize_tire(req_Lm: float, reports=True, res_level=0) -> Tuple[om.Problem, bool]: 
    """This function sets up the MDA problem for openMDAO 

    Args:
        req_Lm (float): the minimum required load capacity 
        reports (bool, optional): should reports be auto generated? 
            Defaults to True. 
        res_level (int, optional): the level of detail should the 
            solver results be printed. Defaults to 0. 

    Returns:
        Tuple[om.Problem, bool]: [
            the optimized MDA problem with results, 
            if the optimization was successful 
        ]
    """
    prob = om.Problem(reports=reports) 
    prob.model = TireMDA()
    prob.driver = om.ScipyOptimizeDriver(optimizer='SLSQP') 
    
    prob.model.add_constraint('Lm', lower=req_Lm) 
    prob.model.approx_totals() 
    
    prob.setup() 
    prob.set_solver_print(level=res_level)
    fail_fag = prob.run_driver() 
    
    return prob, not fail_fag

def eval_optimizer(
    num=30, range_l=1000, range_u=76001, show_plot=False, num_summary=True
) -> float:
    """Test the performance (load capacity of the tires) of the optimization 
    setup by comparing the expected performance to the performance of the 
    optimized model. 

    Args:
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
        Lm -= 1
        succ = False 
        while not succ: 
            Lm += 1
            prob, succ = optimize_tire(Lm, reports=False, res_level=-1)
    
        Dm = prob.get_val('Dm')[0]
        Wm = prob.get_val('Wm')[0]
        D = prob.get_val('D')[0]
        DF = prob.get_val('DF')[0]
        PR = prob.get_val('PR')[0]
        tire = Tire(PR=PR, DoMax=Dm, DoMin=Dm, WMax=Wm, WMin=Wm, RD=D, DF=DF)
        
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
    required_Lm = 36000 
    prob, succ = optimize_tire(required_Lm, reports=False)
    
    Dm = prob.get_val('Dm')[0]
    Wm = prob.get_val('Wm')[0]
    D = prob.get_val('D')[0]
    DF = prob.get_val('DF')[0]
    PR = prob.get_val('PR')[0]
    print("Dm: ", Dm)
    print("Wm: ", Wm)
    print("D: ", D)
    print("DF: ", DF)
    print("PR: ", PR)
    print()
    
    tire = Tire(PR=PR, DoMax=Dm, DoMin=Dm, WMax=Wm, WMin=Wm, RD=D, DF=DF)
    print("Required load capacity:", required_Lm, "lbs")
    print("Load capacity of optimized tire:", tire.max_load_capacity(exact=True), "lbs")
    print("Gas Mass (model):", tire.inflation_medium_mass(), "kg")
    print('Gas Mass (MDA):', prob.get_val('mass')[0], "kg")
    
    # print("Standard Error between required and optimized Lm:", eval_optimizer(show_plot=True))
    