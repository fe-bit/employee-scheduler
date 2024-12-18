
import pandas as pd
from datetime import datetime, date, timedelta, time
import calendar
import enum
import random
from shifts import create_shifts_for_dates, get_shifts_per_employee, CarType
from optimizations.fitness import calculate_fitness



class GeneticAlgorithm:

    def __init__(self, population_size=100, mutation_rate=0.01, crossover_rate=0.8, elitism=True, employees=10):
        self.population_size = population_size
        
        self.muation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.elitism = elitism

        self.shifts = create_shifts_for_dates(12, 2024)
        print(len(self.shifts)*8/employees)
        self.chromosome_length = len(self.shifts)
        n = employees
        self.gene_min = 0
        self.gene_max = n
        # self.employees = {
        #     0: {"name": "Charlie", "qualification": [CarType.KTW_SW, CarType.RTW_SW]}
        # }

        self.employee_preferences = generate_employee_shifts(num_employees=n, month=12, year=2024)
        self.employee_preferences_df = pd.DataFrame.from_records(self.employee_preferences)
        self.employee_idx2id = {i: v for i, v in enumerate(self.employee_preferences_df["employee_id"].unique())} # key: id used for GA; value: id of employee

        self.population = self._initialize_population()

    def _initialize_population(self) -> list[list[int]]:
        """Create initial random population with integer genes."""
        return [
            [random.randint(self.gene_min, self.gene_max) 
             for _ in range(self.chromosome_length)]
            for _ in range(self.population_size)
        ]
    
    
    # def run(self, data:pd.DataFrame):
    #     shifts = create_shifts_of_month(12, 2024)
    #     employee_preferences = generate_employee_shifts(num_employees=10, month=12, year=2024)
    #     employee_preferences_df = pd.DataFrame.from_records(employee_preferences)

    #     # employee_qualifications = {
    #     #     0: [CarType.KTW_D, CarType.RTW_D]
    #     # }
    #     # print(employee_preferences_df)
    #     employee_idx2id = {i: v for i, v in enumerate(employee_preferences_df["employee_id"].unique())} # key: id used for GA; value: id of employee
    #     genes_initial = [random.choices(list(employee_idx2id.keys())) for _ in range(len(shifts))]
    #     self._calculate_fitness(employee_preferences_df, genes_initial, shifts)
    #     return None
    
    def _calculate_fitness(self, chrom):
        return calculate_fitness(self.employee_preferences, chrom, self.shifts)


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
        mutated = chromosome.copy()
        for i in range(len(mutated)):
            if random.random() < self.muation_rate:
                # Random integer mutation within range
                mutated[i] = random.randint(self.gene_min, self.gene_max)
        return mutated
    
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


def generate_employee_shifts(num_employees=10, month=12, year=2024):
    """
    Generate a month of employee shift data with varied preferences
    
    Args:
    - num_employees (int): Number of employees
    - month (int): Month to generate shifts for
    - year (int): Year to generate shifts for
    
    Returns:
    - List of shift dictionaries
    """
    shifts = []
    shift_types = [
        {"start": "06:00:00", "end": "14:00:00"},
        {"start": "14:00:00", "end": "22:00:00"},
        {"start": "22:00:00", "end": "06:00:00"}
    ]
    preferences = ["preferred", "available", "unavailable"]
    
    # Create a list of days in the month
    days = [day for day in range(1, 32) if datetime(year, month, day).month == month]
    
    for employee_id in range(1, num_employees + 1):
        # Ensure each employee gets close to 40 hours per week
        shifts_per_week = random.randint(4, 6)
        
        for week in range(4):  # 4 weeks in month
            weekly_shifts = random.sample(days[week*7:(week+1)*7], shifts_per_week)
            
            for shift_day in weekly_shifts:
                shift_type = random.choice(shift_types)
                preference = random.choices(
                    preferences, 
                    weights=[0.4, 0.4, 0.2]  # More weight to preferred/available
                )[0]
                
                shift = {
                    "employee_id": employee_id,
                    "date_start": f"{year}-{month:02d}-{shift_day:02d} {shift_type['start']}",
                    "date_end": f"{year}-{month:02d}-{shift_day:02d} {shift_type['end']}",
                    "preference": preference
                }
                shifts.append(shift)
    
    return shifts
