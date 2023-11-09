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
from typing import Tuple, Optional, List, Dict
import time 
import numpy as np 
from _models import Tire


class GA_Individual:  
    """A GA individual class for tire design optimization 
    """
    def __init__(self, chromosome) -> None:
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
        if tire.max_load_capacity() < self.chromosome[5]: # req_Lm 
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
    
    def mate(self, par2: 'GA_Individual', scopes: Dict[str, Tuple[float, float]]) -> 'GA_Individual': 
        """Perform mating between two parent GA_Individual and produce a 
        new offspring GA_Individual. 

        Args:
            par2 (GA_Individual): parent 2 of the mating 
            scopes (Dict[str, Tuple[float, float]]): the domain of all design variables 
                Dict[name_of_variable, array_of_all_available_values]

        Returns:
            GA_Individual: the new offspring 
        """
        vars = ["PR", "Dm", "Wm", "D", "DF"]
        child_chromosome = []
        for i, (gp1, gp2) in enumerate(zip(self.chromosome[:-1], par2.chromosome[:-1])): 
            prob = np.random.rand() 
            if prob < 0.45: # insert gene from parent 1 
                child_chromosome.append(gp1)
            elif prob < 0.90: # insert gene from parent 2 
                child_chromosome.append(gp2)
            else: # insert random gene (mutate) to maintain diversity 
                child_chromosome.append(self.mutated_gene(scopes[vars[i]]))
        return GA_Individual(child_chromosome + [self.chromosome[-1]])
        

def ga_opt(
    req_Lm: float, speed_index: float, scopes: Dict[str, Tuple[float, float]], 
    pop_size=20, iter=10000, runtime=15*60, conv_fitness=1e-3
) -> Optional[Tire]: 
    """Use genetic algorithm (GA) to search for an optimized tire design option 
    in the continuous design space. 

    Args:
        req_Lm (float): minimum required loading capability 
        speed_index (float): the speed index of the target aircraft design 
        scopes (Dict[str, Tuple[float, float]]): the domain of all design variables 
            Dict[name_of_variable, array_of_all_available_values]
        pop_size (int, optional): size of the GA population to maintain. 
            Defaults to 10.
        iter (int, optional): stopping criterion in number of iterations. 
            Defaults to 10000.
        runtime (float, optional): stopping criterion in runtime length (sec). 
            Defaults to 15*60.
        conv_fitness (float, optional): stopping criterion in optimization fitness 
            for convergence (% improvement relative to previous iteration). 
            Defaults to 1e-3.
    
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
        gnome = GA_Individual.create_gnome(req_Lm, scopes)
        population.append(GA_Individual(gnome))
    
    curr_best = float('inf')
    
    for i in range(iter): 
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
            child = parent1.mate(parent2, scopes)
            new_generation.append(child)
        population = new_generation

        # Sort population in increasing tire mass 
        population = sorted(population, key=lambda x:x.fitness)
        
        # Check convergence fitness 
        if population[0].fitness < curr_best: 
            if (curr_best - population[0].fitness) / curr_best <= conv_fitness and curr_best != float('inf'): 
                return Tire(
                    PR=population[0].chromosome[0], Dm=population[0].chromosome[1], 
                    Wm=population[0].chromosome[2], D=population[0].chromosome[3], 
                    DF=population[0].chromosome[4]
                )
            else: 
                curr_best = population[0].fitness 
        # Check runtime 
        if time.time() - start_time >= runtime: 
            return Tire(
                PR=population[0].chromosome[0], Dm=population[0].chromosome[1], 
                Wm=population[0].chromosome[2], D=population[0].chromosome[3], 
                DF=population[0].chromosome[4]
            )
        
        if i % 100 == 0: 
            print("Generation No. {}:\tlowest tire mass = {} lbs".format(
                i, population[0].fitness
            ))
    
    return Tire(
        PR=population[0].chromosome[0], Dm=population[0].chromosome[1], 
        Wm=population[0].chromosome[2], D=population[0].chromosome[3], 
        DF=population[0].chromosome[4]
    ) 

if __name__ == "__main__": 
    scopes = {
        "Dm": (12, 56), 
        "Wm": (4, 21), 
        "D": (4, 24), 
        "DF": (5, 33), 
        "PR": (4, 38)
    }
    tire = ga_opt(36000, 0, scopes)
    print(tire)