"""
The optimizer implements the gradients-based optimization method utilizing the openMDAO framework [1], 
developed by NASA. Meanwhile, additional design options are also presented for users' reference from the 
manufacturer's databook (Michelin and Goodyear). 

[1] Gray, J. S., Hwang, J. T., Martins, J. R. R. A., Moore, K. T., & Naylor, B. A. (2019). 
    OpenMDAO: an open-source framework for multidisciplinary design, analysis, and optimization. 
    Structural and Multidisciplinary Optimization, 59(4), 1075–1104. 
    https://doi.org/10.1007/s00158-019-02211-z
"""

import re 
import csv 
import copy 
import numpy as np 
from scipy import constants
from typing import Dict, Tuple, Optional

import openmdao.api as om

from models import Tire


def search_databook(Lm_des: float, speed_index_des=0.0, source='michelin') -> Optional[Tire]:
    """Given the desired loading capacity, find the corresponding tire specifications 
    from the Michelin Tire Databook. 

    Args:
        Lm_des (float): required tire loading capability in lbs. 
        speed_index_des (float, optional): designed speed rating for the aircraft in mph. Defaults to 0.0.
        source (str, optional): source of manufacturer databook from {'michelin', 'goodyear'}. 
            Defaults to 'michelin'. 

    Returns:
        Optional[Tire]: recommended lightest tire based on manufacturer databook. 
    """
    best_tire = None 
    lowest_mass = float('inf') 
    
    if source == 'michelin': 
        with open("manufacturer_data/michelin_bias.csv") as data_csv: 
            csv_reader = csv.reader(data_csv)
            next(csv_reader)  # skip header row
            
            for row in csv_reader:
                # Data clean up 
                manu_dim = ['0' if x == '' else x for x in row[1:-1]] # replace empty elements with '0'
                if 'kt' in manu_dim[4].lower(): # convert kt to mph 
                    manu_dim[4] = float(re.sub('[A-Za-z ]+', '', manu_dim[4]).split()[0]) * constants.knot / constants.mph
                elif 'ls' in manu_dim[4].lower(): # assign 1 mph for LS ratings 
                    manu_dim[4] = '1'
                manu_dim = [float(dim) for dim in manu_dim] # convert all elements to floats

                # Check fitness for consideration 
                if (
                    (manu_dim[5] and manu_dim[9]) and # required design parameters present 
                    manu_dim[5] >= Lm_des and # check if Lm meet requirement 
                    (not speed_index_des or not manu_dim[4] or manu_dim[4] >= speed_index_des) # check if speed index meet requirement (if any)
                ):
                    tire = Tire(
                        D=manu_dim[2], PR=manu_dim[3], SI=manu_dim[4], Lm=manu_dim[5], 
                        DoMax=manu_dim[8], DoMin=manu_dim[9], WMax=manu_dim[10], 
                        WMin=manu_dim[11], RD=manu_dim[18], FH=manu_dim[19], DF=manu_dim[21]
                    )
                    curr_mass = tire.inflation_medium_mass()
                    # Check if better than current best 
                    if curr_mass < lowest_mass: 
                        lowest_mass = curr_mass 
                        best_tire = copy.deepcopy(tire) 
    elif source == 'goodyear': 
        with open("manufacturer_data/goodyear_bias.csv") as data_csv: 
            csv_reader = csv.reader(data_csv)
            next(csv_reader)  # skip header row
            
            for row in csv_reader:
                # Data clean up 
                manu_dim = ['0' if x == '' else x for x in row] # replace empty elements with '0'
                if 'K' in manu_dim[4]: # Check SI (could be in kt or mph or LS)
                    manu_dim[4] = float(manu_dim[4][:-1]) * constants.knot / constants.mph
                
                # Convert all elements to floats
                for i, dim in enumerate(manu_dim): 
                    try: 
                        manu_dim[i] = float(dim)
                    except: 
                        pass 
                
                # Check fitness for consideration 
                if (
                    (manu_dim[5] and manu_dim[12]) and # required design parameters present 
                    manu_dim[5] >= Lm_des and # check if Lm meet requirement 
                    (not speed_index_des or not manu_dim[4] or manu_dim[4] >= speed_index_des) # check if speed index meet requirement (if any)
                ):
                    tire = Tire(
                        D=manu_dim[23], PR=manu_dim[2], SI=manu_dim[4], Lm=manu_dim[5], 
                        DoMax=manu_dim[12], DoMin=manu_dim[13], WMax=manu_dim[14], 
                        WMin=manu_dim[15], RD=manu_dim[23], FH=manu_dim[24]
                    )
                    curr_mass = tire.inflation_medium_mass()
                    # Check if better than current best 
                    if curr_mass < lowest_mass: 
                        lowest_mass = curr_mass 
                        best_tire = copy.deepcopy(tire) 
    else: 
        raise ValueError("Unsupported source, please choose from {'michelin', 'goodyear'}.") 
    
    return best_tire


def _gradients_opt(
    req_Lm: float, speed_index: float, cord_break_load: float, 
    scopes: Dict[str, Tuple[float, float, float]], tol=1e-4
) -> Optional[Tire]: 
    """Use the openMDAO framework to perform gradients-based optimization to search 
    for an optimized aircraft tire design given scopes and solver types. 

    Args:
        req_Lm (float): the minimum required load capacity 
        speed_index (float): the speed index of the target aircraft design 
        cord_break_load (float): cord material designed breaking load in N. 
        scopes (Dict[str, Tuple[float, float, float]]): the domain of all design variables 
            Dict[name_of_variable, Tuple[lower_bound, upper_bound, initial_guess]]
        tol (float, optional): tolerance for termination. Defaults to 1e-4. 
        
    Returns:
        Optional[Tire]: the optimized tire design 
    """
    init_val = {} # take average for initialized values 
    for key, item in scopes.items(): 
        if not item[2] or item[2] < item[0] or item[2] > item[1]: 
            init_val[key] = (item[0] + item[1]) / 2
        else: 
            init_val[key] = item[2]
    
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
            
            tire = Tire(PR=PR, Dm=Dm, Wm=Wm, RD=D, DF=DF, SI=speed_index)
            outputs['Lm'] = tire.max_load_capacity(exact=True)

    class GasMass(om.ExplicitComponent): 
        """The explicit MDA component that defines the objective 
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
            
            tire = Tire(PR=PR, Dm=Dm, Wm=Wm, RD=D, DF=DF, SI=speed_index)
            outputs['mass'] = tire.inflation_medium_mass()
            
    class MechFeasibility(om.ExplicitComponent): 
        """The explicit component that calculates cord load for 
        mechanical feasibility evaluation 
        """
        def setup(self): 
            self.add_input('Dm', val=init_val['Dm'])
            self.add_input('Wm', val=init_val['Wm'])
            self.add_input('D', val=init_val['D'])
            self.add_input('DF', val=init_val['DF'])
            self.add_input('PR', val=init_val['PR'])
            self.add_output('fiber_tension')
        
        def setup_partials(self):
            self.declare_partials('*', '*', method='fd')
        
        def compute(self, inputs, outputs):
            Dm = inputs['Dm']
            Wm = inputs['Wm']
            D = inputs['D']
            DF = inputs['DF']
            PR = inputs['PR']
            
            tire = Tire(PR=PR, Dm=Dm, Wm=Wm, RD=D, DF=DF, SI=speed_index)
            outputs['fiber_tension'] = tire.cord_tension_walter()
            

    class TireMDA(om.Group): 
        """The MDA group that connects all disciplines, 
        objectives, and constraints for optimization. 
        """
        def setup(self):
            cycle = self.add_subsystem('cycle', om.Group())
            cycle.add_subsystem('d', LoadCapacity())
            cycle.add_subsystem('e', MechFeasibility())
            
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
            self.cycle.promotes('e', inputs=['Dm', 'Wm', 'D', 'DF', 'PR'], outputs=['fiber_tension'])
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
    
    prob = om.Problem(reports=False) 
    prob.model = TireMDA()
    prob.driver = om.ScipyOptimizeDriver(optimizer='SLSQP') 
    prob.driver.options['tol'] = tol
    prob.driver.options['disp'] = False
    
    prob.model.add_constraint('Lm', lower=req_Lm) 
    prob.model.add_constraint('fiber_tension', upper=cord_break_load)
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
        PR=prob.get_val('PR')[0], 
        SI=speed_index
    )
    return tire 

def gradients_opt(
    req_Lm: float, speed_index: float, cord_break_load: float, 
    scopes: Dict[str, Tuple[float, float]], tol=1e-4
) -> Tire: 
    """Use the openMDAO framework to perform gradients-based optimization to search 
    for an optimized aircraft tire design given scopes and solver types. 

    Args:
        req_Lm (float): the minimum required load capacity 
        speed_index (float): the speed index of the target aircraft design 
        cord_break_load (float, optional): cord material designed breaking load in N. 
        scopes (Dict[str, Tuple[float, float]]): the domain of all design variables 
            Dict[name_of_variable, Tuple[min_value, max_value, initial_guess]]
        tol (float, optional): tolerance for termination. Defaults to 1e-4. 

    Returns:
        Tire: the optimized tire design 
    """
    tire = None 
    counter = 0 
    while not tire: 
        counter += 1
        tire = _gradients_opt(req_Lm, speed_index, cord_break_load, scopes, tol=tol)
        req_Lm += 1
        if counter == 10: 
            break 
    return tire 
