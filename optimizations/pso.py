"""
The particle swarm optimization (PSO) method employs multiple agents to navigate 
the design space simultaneously. Meanwhile, each agent benefits from the experience 
of all other agents during the searching process. Consequently, all particles 
should converge to an optimal point in the design space as defined by the 
heuristic (objective) function. 

Reference: https://machinelearningmastery.com/a-gentle-introduction-to-particle-swarm-optimization/ 
"""

import time 
from typing import Optional, Tuple, Union, Dict, List 

import numpy as np 
import matplotlib.pyplot as plt 

from _models import Tire 
from selector import search_databook


class PSO_Particle: 
    """A Particle (searching agent) class for PSO 
    """
    def __init__(self, req_Lm: float, scopes: Dict[str, Tuple[float, float]]) -> None:
        """
        Args:
            req_Lm (float): minimum required loading capability 
            scopes (Dict[str, Tuple[float, float]]): the domain of all design variables 
                Dict[name_of_variable, Tuple[min_value, max_value]]
        """
        position = [] 
        for key in ["PR", "Dm", "Wm", "D", "DF"]: 
            position.append(scopes[key][0] + np.random.rand() * (scopes[key][1] - scopes[key][0]))
        
        self.req_Lm = req_Lm
        self.position = np.array(position)
        self.velocity = np.random.rand(len(position))
        self.best_position = self.position.copy()
        self.best_obj = self.calc_obj()
    
    def calc_obj(self) -> float: 
        """Calculate the tire mass (objective) for its current position in the design space. 

        Returns:
            float: tire mass 
        """
        # self.chromosome: [PR, Dm, Wm, D, DF]
        asp_ratio = (self.position[1] - self.position[3]) / 2 / self.position[2] 
        if (
            self.position[1] <= self.position[4] or # Dm <= DF
            self.position[4] <= self.position[3] or # DF <= D
            asp_ratio < 0.5 or asp_ratio > 1
        ): 
            return float('inf')
        tire = Tire(
            PR=self.position[0], Dm=self.position[1], Wm=self.position[2], 
            D=self.position[3], DF=self.position[4]
        )
        if tire.max_load_capacity(exact=True) < self.req_Lm: # req_Lm 
            return float('inf')
        if not tire.is_mech_feasible(): 
            return float('inf')
        return tire.inflation_medium_mass() 
    
    def update_position(self, c1: float, c2: float, w: float, gbest_pos: List[float]) -> float: 
        """Find and update the next position for the particle 

        Args:
            c1 (float): cognitive coefficient
            c2 (float): social coefficient
            w (float): inertia weight constant
            gbest_pos (List[float]): position of the global best position found

        Returns:
            float: new best objective value of the particle 
        """
        self.velocity = w * self.velocity + c1 * np.random.rand() * (
            self.best_position - self.position
        ) + c2 * np.random.rand() * (gbest_pos - self.position)
        self.position = self.position + self.velocity
        
        new_obj = self.calc_obj() 
        if new_obj <= self.best_obj: 
            self.best_obj = new_obj 
            self.best_position = self.position.copy() 
        
        return new_obj


def pso_opt(
    req_Lm: float, speed_index: float, scopes: Dict[str, Tuple[float, float]], 
    n_particles=20, c1=0.1, c2=0.1, w=0.8, n_iter=1000, runtime=15*60, 
    conv_fitness=1e-3, print_steps=-1 
) -> Optional[Tire]: 
    """Perform particle swarm optimization 

    Args:
        req_Lm (float): minimum required loading capability 
        speed_index (float): the speed index of the target aircraft design 
        scopes (Dict[str, Tuple[float, float]]): the domain of all design variables 
            Dict[name_of_variable, Tuple[min_value, max_value]]
        n_particles (int, optional): number of particles. Defaults to 20.
        c1 (float, optional): cognitive coefficient. Defaults to 0.1.
        c2 (float, optional): social coefficient. Defaults to 0.1.
        w (float, optional): inertia weight constant between 0 and 1. Defaults to 0.8.
        n_iter (int, optional): maxinum number of iterations. Defaults to 1000.
        runtime (_type_, optional): maximum runtime length (seconds). Defaults to 15*60.
        conv_fitness (_type_, optional): stopping criterion in optimization fitness of 
            convergence (% improvement in global optimum found relative to previous
            iteration). Defaults to 1e-3.
        print_steps (int, optional): -1: print nothing, 0: print when completed only, 
            ≥ 1 for results after every print_steps of generations. Defaults to -1.

    Returns:
        Optional[Tire]: the optimized tire design located within stopping criteria. 
    """
    # Initialize particles 
    particles = []
    for _ in range(n_particles): 
        while True: 
            p = PSO_Particle(req_Lm, scopes) 
            if p.best_obj < float('inf'): 
                break 
        particles.append(p)
    
    ind_best = np.argmin([p.best_obj for p in particles])
    global_best_position = particles[ind_best].position
    global_best_obj = particles[ind_best].best_obj
    
    st = time.time() 
    for i in range(n_iter): 
        for p in particles: 
            pbest = p.update_position(c1, c2, w, global_best_position)
            if pbest < global_best_obj: 
                # Check convergence fitness 
                if (global_best_obj - pbest) / global_best_obj <= conv_fitness: 
                    if print_steps >= 0: 
                        print("Convergence fitness satisfied after {} iterations".format(i))
                    return Tire(
                        PR=p.position[0], Dm=p.position[1], Wm=p.position[2], D=p.position[3], 
                        DF=p.position[4]
                    )
                global_best_obj = pbest 
                global_best_position = p.position
            if time.time() - st >= runtime: 
                if print_steps >= 0: 
                    print("Runtime limit reached after {} iterations".format(i))
                return Tire(
                    PR=p.position[0], Dm=p.position[1], Wm=p.position[2], D=p.position[3], 
                    DF=p.position[4]
                )
        if print_steps > 0 and i % print_steps == 0: 
            print("Iteration No. {}: lowest tire mass = {} kg".format(i, global_best_obj))
    
    return Tire(
        PR=global_best_position[0], Dm=global_best_position[1], Wm=global_best_position[2], 
        D=global_best_position[3], DF=global_best_position[4]
    )
    

def eval_pso(
    scopes: Dict[str, Tuple[float, float]], n_particles: int, c1: float, c2: float, 
    w: float, Lm_testing_range=(2000, 72000), Lm_step=10000, iter_per_Lm=3, 
    show_plot=True, n_iter=10000, runtime=15*60, conv_fitness=1e-3 
) -> Union[float, float]: 
    """Algorithmic evaluation of the GA optimization method. 

    Args:
        scopes (Dict[str, Tuple[float, float]]): same to the scopes provided to 
            the algorithm input. 
        pop_size (int): size of the GA population to maintain. 
        prob_mutate (float): the probability of mutation for every mating. 
        use_init_gene (bool): use the reference tire option as the initial 
            gene to start the evolution with. 
        Lm_testing_range (tuple, optional): lower and upper bound of Lm for testing. 
            Defaults to (2000, 72000).
        Lm_step (int, optional): step size for Lm to be tested. Defaults to 10000.
        iter_per_Lm (int, optional): number of tests for every Lm tested. 
            Defaults to 3.
        show_plot (bool, optional): show the comparison plot. Defaults to True. 
        n_iter (int, optional): stopping criterion in number of iterations. 
            Defaults to 10000.
        runtime (float, optional): stopping criterion in runtime length (sec). 
            Defaults to 15*60.
        conv_fitness (float, optional): stopping criterion in optimization fitness 
            for convergence (% improvement relative to previous iteration). 
            Defaults to 1e-3.
    
    Returns: 
        Union[float, float]: optimality and efficiency of the testing pop_size. 
    """
    testing_Lm = np.arange(Lm_testing_range[0], Lm_testing_range[1] + Lm_step, Lm_step)
    opt_Lm, opt_mass, opt_AR, time_used = [], [], [], []
    
    for Lm in testing_Lm: 
        temp_Lm, temp_mass, temp_AR, temp_time = [], [], [], [] 
        ref_tire = search_databook(Lm)
        for _ in range(iter_per_Lm): 
            s_time = time.time() 
            tire = pso_opt(
                Lm, 0, scopes, n_particles=n_particles, c1=c1, c2=c2, w=w, 
                n_iter=n_iter, runtime=runtime, conv_fitness=conv_fitness
            )
            temp_time.append(time.time() - s_time)
            temp_Lm.append(tire.max_load_capacity(exact=True) - Lm)
            temp_mass.append(ref_tire.inflation_medium_mass() - tire.inflation_medium_mass())
            temp_AR.append(tire.aspect_ratio())
        opt_Lm.append(temp_Lm)
        opt_mass.append(temp_mass)
        opt_AR.append(temp_AR)
        time_used.append(temp_time)
    
    optimality = np.mean([np.mean(item) for item in opt_mass])
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
        plt.tight_layout() 
        plt.show() 

        # Performance results plot 
        _, ax = plt.subplots()
        ax.boxplot(time_used)
        ax.set_ylabel("Time used per optimization [sec]")
        ax.set_xticks(np.arange(1, len(testing_Lm) + 1))
        ax.set_xticklabels(testing_Lm, rotation=90)
        ax.set_xlabel("Lm(des) [lbs]")
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
    
    tire = pso_opt(36000, 0, scopes, conv_fitness=1e-6, print_steps=True)
    print(tire)
    
    # np.random.seed(80)
    # opt, eff = eval_pso(scopes, 35, 0.1, 0.15, 0.75, Lm_testing_range=(2000, 72000), conv_fitness=1e-8)
    # print("Optimality: {}, efficiency: {}".format(opt, eff))
    
    # eval_opt, eval_eff = [], []
    # testing_pop_size = np.arange(10, 55, 5)
    # for i in testing_pop_size: 
    #     opt, eff = eval_pso(
    #         scopes, i, 0.1, 0.15, 0.75, Lm_testing_range=(2000, 62000), conv_fitness=1e-6, show_plot=False
    #     )
    #     eval_opt.append(opt)
    #     eval_eff.append(eff)
    # print(eval_opt)
    # print(eval_eff)
    # plt.plot(testing_pop_size, eval_opt, label="Optimality")
    # plt.plot(testing_pop_size, eval_eff, label="Efficiency")
    # plt.legend() 
    # plt.show() 