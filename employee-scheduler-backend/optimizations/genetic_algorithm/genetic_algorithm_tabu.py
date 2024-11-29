
import random
from shifts import Shift
from optimizations.fitness import calculate_fitness
import hashlib
from optimizations.preference_encoder import encode_preferences



class GeneticAlgorithmTabu:

    def __init__(self, shifts:list[Shift], population_size=100, mutation_rate=0.01, crossover_rate=0.8, elitism=True, employees=10, preferences={}):
        self.population_size = population_size
        
        self.muation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.elitism = elitism

        self.shifts = shifts
        
        print(len(self.shifts)*8/employees)
        self.chromosome_length = len(self.shifts)
        n = employees
        self.gene_min = 1
        self.gene_max = n

        self.tabu_chromes = set()
        self.population = self._initialize_population()

        self.preferences = encode_preferences(preferences, employees, shifts)

        

    def _initialize_population(self) -> list[list[int]]:
        """Create initial random population with integer genes."""
        pop = [
            [random.randint(self.gene_min, self.gene_max) 
             for _ in range(self.chromosome_length)]
            for _ in range(self.population_size)
        ]
        for p in pop:
            p_hash = self.hash_int_list(p)
            self.tabu_chromes.add(p_hash)

        return pop
            
    def hash_int_list(self, int_list):
        str_list = ''.join(str(num) for num in int_list)
        hash_object = hashlib.md5(str_list.encode())
        hex_dig = hash_object.hexdigest()
        return hex_dig
    
    def _calculate_fitness(self, chrom):
        return calculate_fitness(chrom, self.shifts, self.preferences)


    def _select_parent(self, fitness_values: list[float]) -> list[int]:
        """Select parent using tournament selection."""
        tournament_size = 3
        tournament_indices = random.sample(range(self.population_size), tournament_size)
        tournament_fitness = [fitness_values[i] for i in tournament_indices]
        winner_index = tournament_indices[tournament_fitness.index(max(tournament_fitness))]
        return self.population[winner_index]
    
    def _crossover(self, parent1: list[int], parent2: list[int]) -> tuple[list[int], list[int]]:
        """Perform crossover between two parents."""
        if random.random() < self.crossover_rate:
            # Two-point crossover
            points = sorted(random.sample(range(self.chromosome_length), 2))
            child1 = parent1[:points[0]] + parent2[points[0]:points[1]] + parent1[points[1]:]
            child2 = parent2[:points[0]] + parent1[points[0]:points[1]] + parent2[points[1]:]
            return child1, child2
        return parent1.copy(), parent2.copy()
    
    def _mutate(self, chromosome: list[int]) -> list[int]:
        """Apply mutation to a chromosome."""
        while True:
            mutated = chromosome.copy()
            for i in range(len(mutated)):
                if random.random() < self.muation_rate:
                    # Random integer mutation within range
                    mutated[i] = random.randint(self.gene_min, self.gene_max)
            if h:=self.hash_int_list(mutated) not in self.tabu_chromes:
                self.tabu_chromes.add(h)
                return mutated
            else:
                print("Tabu")
    
    def evolve(self, generations: int, target_fitness = None) -> tuple[list[int], float, list[float]]:
        """
        Evolve the population for the specified number of generations.
        
        Args:
            generations: Number of generations to evolve
            target_fitness: Optional target fitness value to stop early
            
        Returns:
            Tuple containing:
            - Best chromosome found
            - Best fitness value
            - List of best fitness values per generation
        """
        best_fitness_history = []
        best_chromosome = None
        best_fitness = float('-inf')
        
        for generation in range(generations):
            # Calculate fitness for all chromosomes
            fitness_values = [self._calculate_fitness(chrom) for chrom in self.population]
            
            # Track best solution
            generation_best_fitness = max(fitness_values)
            generation_best_index = fitness_values.index(generation_best_fitness)
            generation_best_chromosome = self.population[generation_best_index]
            
            if generation_best_fitness > best_fitness:
                best_fitness = generation_best_fitness
                best_chromosome = generation_best_chromosome.copy()
            
            best_fitness_history.append(best_fitness)
            
            # Check if target fitness is reached
            if target_fitness is not None and best_fitness >= target_fitness:
                break
            
            # Create new population
            new_population = []
            
            # Elitism: preserve best solution
            if self.elitism:
                new_population.append(generation_best_chromosome)
            
            # Generate new individuals
            while len(new_population) < self.population_size:
                # Select parents
                parent1 = self._select_parent(fitness_values)
                parent2 = self._select_parent(fitness_values)
                
                
                # Create offspring
                child1, child2 = self._crossover(parent1, parent2)
                
                # Mutate offspring
                child1 = self._mutate(child1)
                child2 = self._mutate(child2)
                
                new_population.extend([child1, child2])
            
            # Ensure population size remains constant
            self.population = new_population[:self.population_size]
            if len(best_fitness_history) > 1 and best_fitness != best_fitness_history[-2]:
                print(best_fitness)
        
        return best_chromosome, best_fitness, best_fitness_history
