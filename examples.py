from ann import CreateNetwork
from ann import GetWeightLen
from ga import AG
from ga import Chromosome


# Create Population of 10 individuous randomly from specific topology 2 inputs 6,1 layers
population_random = AG.Random(10,GetWeightLen(2,[6,1]))

# Load population from a list
c = []
for value in value_list:
    c.append(Chromosome(value))

polulation = AG(c)

# Generate ANN Json from population individouos
for pop in population_random.polulation:
    ann = CreateNetwork(2, [6,1], pop.value, json=True, outputs_types=['discrete'])


# Load fitness in AG from fitness list (in same order)
for i in random(0, len(fitness_list)):
    population_random.polulation[i].fitness = fitness_list[i]


# Go to next generation
population_random.next_generation_cx_simple()

