import openmdao.api as om
from models import Tire

class LoadCapacity(om.ExplicitComponent): 
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
        
if __name__ == "__main__": 
    prob = om.Problem() 
    prob.model.add_subsystem(
        'load', LoadCapacity(), promotes_inputs=['Dm', 'Wm', 'D', 'DF', 'PR'], 
        promotes_outputs=['Lm']
    )
    prob.model.nonlinear_solver = om.NonlinearBlockGS() 
    prob.model.add_subsystem(
        'obj', GasMass(), promotes_inputs=['Dm', 'Wm', 'D', 'DF', 'PR'], 
        promotes_outputs=['mass']
    )
    prob.model.add_subsystem(
        'con_cmp1', om.ExecComp('con1 = mass'), promotes=['con1', 'mass']
    )
    
    prob.driver = om.ScipyOptimizeDriver() 
    prob.driver.options['optimizer'] = 'SLSQP'
    
    prob.model.add_design_var('Dm', lower=12, upper=57)
    prob.model.add_design_var('Wm', lower=4, upper=21)
    prob.model.add_design_var('D', lower=4, upper=28)
    prob.model.add_design_var('DF', lower=5.1, upper=33)
    prob.model.add_design_var('PR', lower=4, upper=38)
    prob.model.add_objective("mass")
    prob.model.add_constraint('con1', lower=0.01)
    prob.model.add_constraint('Lm', lower=10000) # add required Lm here 
    
    prob.model.approx_totals() 
    
    prob.setup() 
    prob.set_solver_print(level=0)
    prob.run_driver() 
    
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
    
    tire = Tire(PR=PR, DoMax=Dm, DoMin=Dm, WMax=Wm, WMin=Wm, RD=D, DF=DF)
    print("Load Capacity:", tire.max_load_capacity(exact=True))
    print("Gas Mass (model):", tire.inflation_medium_mass())
    print('Gas Mass (MDA):', prob.get_val('mass')[0])
    