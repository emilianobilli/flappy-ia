import random
import copy


class Chromosome(object):
    @classmethod
    def Random(cls, size, i_min=-1, i_max=1):
        return cls([random.uniform(i_min, i_max) for i in range(0,size)])
    
    def __init__(self, value: list, fitness=None):
        self.value = value
        self.fitness = fitness

    def __repr__(self):
        return str(self.value)

    def __eq__(self, other):
        if len(self.value) != len(other.value):
            return False

        for i in range(0,len(self.value)):
            if self.value[i] != other.value[i]:
                return False
        
        return True


    def mutate(self, mu_min=-2, mu_max=2):
        # Select who gen mutate 
        i = random.randint(0, len(self.value)-1)
        # Select operations 0 add, 1 sub
        self.value[i] = self.value[i] + random.uniform(mu_min,mu_max)


    def cross_simple(self, other):
        if len(other.value) != len(self.value):
            raise ValueError('Impossible Cross diferent sizes')
        v1 = []
        v2 = []
        for i in range(0,len(self.value)):
            if random.uniform(0,1) < 0.5:
                v1.append(other.value[i])
                v2.append(self.value[i])
            else:
                v1.append(self.value[i])
                v2.append(other.value[i])

        return Chromosome(v1), Chromosome(v2)


    def cross_arithmetic(self, other):
        if len(other.value) != len(self.value):
            raise ValueError('Impossible Cross diferent sizes')
        
        v1 = []
        v2 = []
        
        for i in range(0,len(self.value)):
            if random.uniform(0,1) < 0.5:
                v1.append(self.value[i])
                v2.append(other.value[i])
            else:
                v = (self.value[i] + other.value[i]) / 2
                v1.append(v)
                v2.append(v)
        
        return Chromosome(c1), Chromosome(c2)

class AG(object):
    
    @classmethod
    def Random(cls, polulation_len, gen_len):
        return cls([Chromosome.Random(gen_len) for i in range(0,polulation_len)],None)

    def __init__(self, chromosome_list=None, fitness_list=None):
        if chromosome_list is None:
            raise ValueError('Invalid argument')

        self.p_cx = 0.9
        self.p_mu = 0.3
        self.mu_min = -2
        self.mu_max = 2
        self.elitist = True

        self.polulation = []
        if fitness_list is not None and len(chromosome_list) != len(fitness_list):
            raise ValueError('Impossible to init the AG')
    
        for i in range(0,len(chromosome_list)):
            c = chromosome_list[i]
            if fitness_list is not None:
                c.fitness = fitness_list[i]
            else:
                c.fitness = None
            self.polulation.append(c)


    def get_winner(self, fitness_max=True):
        if len(self.polulation) == 0:
            return None
        
        value = self.polulation[0].fitness
        win   = self.polulation[0]

        for pop in self.polulation:
            if fitness_max:
                if pop.fitness > value:
                    value = pop.fitness
                    win   = pop
            else:
                if pop.fitness < value:
                    value = pop.fitness
                    win   = pop

        return Chromosome(win.value)

    def tournament(self, k=3, fitness_max=True):
        def key(v):
            return v.fitness

        n = random.sample(self.polulation, k)
        n.sort(reverse=fitness_max, key=key)

        return n

    @staticmethod
    def chromosome_in_list(chromosome:Chromosome, chromosome_list: list) -> bool:
        for obj in chromosome_list:
            if chromosome == obj:
                return True
        return False 


    def next_generation_cx_simple(self, k=3, fitness_max=True):
        next_generation = []
        polulation_len = len(self.polulation)


        if self.elitist:
            next_generation.append(self.get_winner(fitness_max))

        while len(next_generation) < polulation_len:
            wins = self.tournament(k, fitness_max)
            c1, c2 = wins[0], wins[1]
            # Return two new Chromosomes
            if random.uniform(0,1) < self.p_cx:
                c1, c2 = c1.cross_simple(c2)

            if random.uniform(0,1) < self.p_mu:
                c1.mutate(self.mu_min,self.mu_max)

            if random.uniform(0,1) < self.p_mu:
                c2.mutate(self.mu_min,self.mu_max)

            if not self.chromosome_in_list(c1,next_generation):
                next_generation.append(c1)

            if not self.chromosome_in_list(c2,next_generation) and len(next_generation) < polulation_len:
                next_generation.append(c2)

        self.polulation = next_generation

    def next_generation_cx_one_point(self, k=3, fitness_max=True):
        next_generation = []
        polulation_len = len(self.polulation)

        if self.elitist:
            next_generation.append(self.get_winner(fitness_max))

        while len(next_generation) < polulation_len:
            wins = self.tournament(k,fitness_max)
            c1, c2 = wins[0], wins[1]

            if random.uniform(0,1) < self.p_cx:
                c1, c2 = c1.cross_arithmetic(c2)
            
            if random.uniform(0,1) < self.p_mu:
                c1.mutate(self.mu_min,self.mu_max)
            if random.uniform(0,1) < self.p_mu:
                c2.mutate(self.mu_min,self.mu_max)

            if not self.chromosome_in_list(c1,next_generation):
                next_generation.append(c1)

            if not self.chromosome_in_list(c2,next_generation) and len(next_generation) < polulation_len:
                next_generation.append(c2)

        self.polulation = next_generation


if __name__ == '__main__':
    import math
    from ann import CreateNetwork
    from ann import GetWeightLen
    from flappy import Game

    polulation = AG.Random(10,GetWeightLen(2,[6,1]))

    generations = 0
    while generations < 20:
        ind = 0
        for pop in polulation.polulation:
            game = Game(0, ind, generations)
            game.brain = CreateNetwork(2, [6,1], pop.value) #, json=True,outputs_types=['discrete'])
            pop.fitness = game.start()
            print('Ind: %d - Fitness: %d - Generation: %d' % (ind, pop.fitness, generations))
            ind = ind + 1

        polulation.next_generation_cx_simple()
        generations = generations + 1
        

