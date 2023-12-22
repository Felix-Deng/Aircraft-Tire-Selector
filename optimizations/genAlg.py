"""
The genetic algorithm (GA) is a more intelligent exploitation of random search. 
Initial individuals are selected from the population to simulate the process of 
natural selection, until the fittest individual is left. 

General algorithm: 
1. Randomly initialize populations P with size n individuals 
2. Determine the fitness of the population (with objective function)
3. Untiil convergence, repeat: 
    i.   Select parents from population 
    ii.  Crossover and generate new population 
    iii. Perform mutation on new population 
    iv.  Calculate fitness for new population 
    
Reference: https://www.geeksforgeeks.org/genetic-algorithms/ 
"""
import time 
import copy 
from typing import Tuple, Optional, Union, List, Dict
import numpy as np 
import matplotlib.pyplot as plt 

from _models import Tire
from selector import search_databook 


class GA_Individual:  
    """A GA individual class for tire design optimization 
    """
    def __init__(self, chromosome: List[float]) -> None:
        self.chromosome = chromosome # List[PR, Dm, Wm, D, DF, req_Lm]
        self.fitness = self.cal_fitness() 
        
    def cal_fitness(self) -> float: 
        """Use the objective function (tire mass) as the fitness score of the 
        individual. Assign infinite mass for not feasible individuals. 

        Returns:
            float: fitness score (i.e., tire mass)
        """
        # self.chromosome: [PR, Dm, Wm, D, DF, req_Lm]
        asp_ratio = (self.chromosome[1] - self.chromosome[3]) / 2 / self.chromosome[2] 
        if (
            self.chromosome[1] <= self.chromosome[4] or # Dm <= DF
            self.chromosome[4] <= self.chromosome[3] or # DF <= D
            asp_ratio < 0.5 or asp_ratio > 1
        ): 
            return float('inf')
        tire = Tire(
            PR=self.chromosome[0], Dm=self.chromosome[1], Wm=self.chromosome[2], 
            D=self.chromosome[3], DF=self.chromosome[4]
        )
        if tire.max_load_capacity(exact=True) < self.chromosome[5]: # req_Lm 
            return float('inf')
        if not tire.is_mech_feasible(): 
            return float('inf')
        return tire.inflation_medium_mass() 
    
    @classmethod 
    def mutated_gene(self, scope: Tuple[float, float]) -> float: 
        """Create a random gene for mutation. 

        Args:
            scope (Tuple[float, float]): scope of the gene to mutate in Tuple[min, max]  

        Returns:
            float: value of the randomly mutated gene within the scope 
        """
        return scope[0] + np.random.rand() * (scope[1] - scope[0]) 
    
    @classmethod
    def create_gnome(self, req_Lm: float, scopes: Dict[str, Tuple[float, float]]) -> List[float]: 
        """Create chromosome: a float array of genes with the key tire design variables 
        and the required loading capability. 

        Args:
            req_Lm (float): minimum required loading capability 
            scopes (Dict[str, Tuple[float, float]]): the domain of all design variables 
                Dict[name_of_variable, array_of_all_available_values]

        Returns:
            List[float]: the created randomized chromosome: List[PR, Dm, Wm, D, DF, req_Lm]
        """
        return [
            self.mutated_gene(scopes[var]) for var in ["PR", "Dm", "Wm", "D", "DF"]
        ] + [req_Lm]
    
    def mate(
        self, par2: 'GA_Individual', scopes: Dict[str, Tuple[float, float]], prob_mutate=0.1
    ) -> 'GA_Individual': 
        """Perform mating between two parent GA_Individual and produce a 
        new offspring GA_Individual. 

        Args:
            par2 (GA_Individual): parent 2 of the mating 
            scopes (Dict[str, Tuple[float, float]]): the domain of all design variables 
                Dict[name_of_variable, array_of_all_available_values]
            prob_mutate (float, optional): the probability of mutation for every mating. 
                Defaults to 0.1. 
        
        Raise: 
            ValueError: prob_mutate must be between 0 and 1. 

        Returns:
            GA_Individual: the new offspring 
        """
        if prob_mutate > 1 or prob_mutate < 0: 
            raise ValueError("prob_mutate must be between 0 and 1.")
        vars = ["PR", "Dm", "Wm", "D", "DF"]
        child_chromosome = []
        for i, (gp1, gp2) in enumerate(zip(self.chromosome[:-1], par2.chromosome[:-1])): 
            prob = np.random.rand() 
            if prob < (1 - prob_mutate) / 2: # insert gene from parent 1 
                child_chromosome.append(gp1)
            elif prob < 1 - prob_mutate: # insert gene from parent 2 
                child_chromosome.append(gp2)
            else: # insert random gene (mutate) to maintain diversity 
                child_chromosome.append(self.mutated_gene(scopes[vars[i]]))
        return GA_Individual(child_chromosome + [self.chromosome[-1]])
        

def ga_opt(
    req_Lm: float, speed_index: float, scopes: Dict[str, Tuple[float, float]], 
    pop_size=20, prob_mutate=0.1, init_gene=[], n_iter=10000, runtime=15*60, conv_fitness=1e-3, 
    print_steps=-1 
) -> Optional[Tire]: 
    """Use genetic algorithm (GA) to search for an optimized tire design option 
    in the continuous design space. 

    Args:
        req_Lm (float): minimum required loading capability 
        speed_index (float): the speed index of the target aircraft design 
        scopes (Dict[str, Tuple[float, float]]): the domain of all design variables 
            Dict[name_of_variable, array_of_all_available_values]
        pop_size (int, optional): size of the GA population to maintain. 
            Defaults to 20.
        prob_mutate (float, optional): the probability of mutation for every mating. 
            Defaults to 0.1. 
        init_gene (list, optional): the initial gene to start the evolution with. 
            Defaults to []. 
        n_iter (int, optional): stopping criterion in number of iterations. 
            Defaults to 10000.
        runtime (float, optional): stopping criterion in runtime length (sec). 
            Defaults to 15*60.
        conv_fitness (float, optional): stopping criterion in optimization fitness 
            for convergence (% improvement relative to previous iteration). 
            Defaults to 1e-3.
        print_steps (int, optional): -1: print nothing, 0: print when completed only, 
            ≥ 1 for results after every print_steps of generations. Defaults to -1.
    
    Raises:
        ValueError: if pop_size < 3

    Returns:
        Optional[Tire]: the optimized tire design located within stopping criteria. 
    """
    # Sanity check 
    if pop_size < 3: 
        raise ValueError("Population size needs to be ≥ 3 to be effective.")
    
    start_time = time.time()
    population = []
    
    # Create initial population 
    for _ in range(pop_size): 
        if not init_gene: 
            gnome = GA_Individual([0.01, 0.01, 0.01, 0.01, 0.01, req_Lm])
            while gnome.fitness == float('inf'): 
                gnome = GA_Individual.create_gnome(req_Lm, scopes)
                gnome = GA_Individual(gnome)
        else: 
            gnome = GA_Individual(copy.deepcopy(init_gene))
        population.append(gnome)
    
    population = sorted(population, key=lambda x:x.fitness)
    curr_best = population[0].fitness
    
    for i in range(n_iter): 
        # Perform Elitism, only 10% of fittest population (or 1 individual if pop_size <=10) 
        # goes to the next generation 
        new_generation = []
        if pop_size <= 10: 
            s = 1 
        else: 
            s = int(pop_size * 0.1)
        new_generation.extend(population[:s])
        
        # The 50% fittest population will mate to produce offspring to fill the rest of 
        # the next generation 
        s = pop_size - s 
        for _ in range(s): 
            parent1 = np.random.choice(population[:int(pop_size*0.5)])
            parent2 = np.random.choice(population[:int(pop_size*0.5)])
            child = parent1.mate(parent2, scopes, prob_mutate)
            new_generation.append(child)
        population = new_generation

        # Sort population in increasing tire mass 
        population = sorted(population, key=lambda x:x.fitness)
        
        # Check convergence fitness 
        if population[0].fitness < curr_best: 
            if (curr_best - population[0].fitness) / curr_best <= conv_fitness and curr_best != float('inf'): 
                if print_steps >= 0: 
                    print("Convergence fitness satisfied after {} generations".format(i))
                return Tire(
                    PR=population[0].chromosome[0], Dm=population[0].chromosome[1], 
                    Wm=population[0].chromosome[2], D=population[0].chromosome[3], 
                    DF=population[0].chromosome[4]
                )
            else: 
                curr_best = population[0].fitness 
        # Check runtime 
        if time.time() - start_time >= runtime: 
            if print_steps >= 0: 
                print("Runtime limit reached after {} generations".format(i))
            return Tire(
                PR=population[0].chromosome[0], Dm=population[0].chromosome[1], 
                Wm=population[0].chromosome[2], D=population[0].chromosome[3], 
                DF=population[0].chromosome[4]
            )
        
        if print_steps > 0 and i % print_steps == 0: 
            print("Generation No. {}:\tlowest tire mass = {} kg".format(
                i, population[0].fitness
            ))
    
    return Tire(
        PR=population[0].chromosome[0], Dm=population[0].chromosome[1], 
        Wm=population[0].chromosome[2], D=population[0].chromosome[3], 
        DF=population[0].chromosome[4]
    ) 


def eval_ga(
    scopes: Dict[str, Tuple[float, float]], pop_size: int, prob_mutate: float, 
    use_init_gene: bool, Lm_testing_range=(2000, 72000), Lm_step=10000, iter_per_Lm=3, 
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
        if use_init_gene: 
            ref_gene = [ref_tire.PR, ref_tire.Dm, ref_tire.Wm, ref_tire.D, ref_tire.DF, Lm] 
        else: 
            ref_gene = [] 
        for _ in range(iter_per_Lm): 
            s_time = time.time() 
            tire = ga_opt(
                Lm, 0, scopes, pop_size=pop_size, prob_mutate=prob_mutate, init_gene=ref_gene, 
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
    
    tire = ga_opt(36000, 0, scopes, pop_size=35, prob_mutate=0.3, print_steps=True)
    print(tire)
    
    # np.random.seed(80)
    # opt, eff = eval_ga(scopes, 35, 0.3, use_init_gene=False, conv_fitness=1e-4)
    # print("Optimality: {}, efficiency: {}".format(opt, eff))
    
    # eval_opt, eval_eff = [], []
    # testing_pop_size = np.arange(10, 55, 5)
    # # testing_mutate_prob = np.arange(0.1, 0.6, 0.1)
    # for i in testing_pop_size: 
    # # for i in testing_mutate_prob: 
    #     opt, eff = eval_ga(scopes, i, 0.15, use_init_gene=False, show_plot=False)
    #     # opt, eff = eval_ga(scopes, 35, i, use_init_gene=False, show_plot=False)
    #     eval_opt.append(opt)
    #     eval_eff.append(eff)
    # print(eval_opt)
    # print(eval_eff)
    # plt.plot(testing_pop_size, eval_opt, label="Optimality")
    # plt.plot(testing_pop_size, eval_eff, label="Efficiency")
    # plt.legend() 
    # plt.show() 