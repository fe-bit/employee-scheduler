from shifts import create_shifts_of_month, get_shifts_per_employee, CarType
from optimizations.fitness import calculate_fitness

class BruteForce:
    def __init__(self, employees):
        self.employees = employees
        self.shifts = create_shifts_of_month(12, 2024)

    def run(self):
        best_chromosome = None
        best_fitness = None
        best_fitness_history = []

        for chrom in generate_combinations(len(self.shifts), 0, self.employees):
            fitness = calculate_fitness(None, chrom, self.shifts)
            if best_fitness is None or fitness > best_fitness:
                best_fitness = fitness
                best_chromosome = chrom
                best_fitness_history.append(fitness)
                print(best_chromosome)
                print(fitness)


        return best_chromosome, best_fitness, best_fitness_history

def generate_combinations(length, min_value, max_value):
    """
    Generates all possible combinations of numbers between 0 and 10 of a given length.

    Args:
        length: The desired length of the combinations.

    Yields:
        A list of integers representing a combination.
    """

    indices = [0] * length
    while True:
        yield [indices[i] for i in range(length)]

        # Increment the rightmost index
        i = length - 1
        while i >= min_value:
            indices[i] += 1
            if indices[i] <= max_value:
                break
            indices[i] = 0
            i -= 1

        # If all indices are 10, we're done
        if i < 0:
            break
