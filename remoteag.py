import requests
from ann import Network

class ServiceLayer(object):
    def __init__(self, provider):
        print(provider)
        self.provider = provider + '/' if not provider.endswith('/') else provider
    
    def new_population(self):
        url = self.provider + '/api/v1/population/'
        ret = requests.post(url)
        if ret.status_code == 201:
            return ret.json()
        return None

    def get_population(self, population_id:str):
        url = self.provider + '/api/v1/population/%s' % population_id
        ret = requests.get(url)
        if ret.status_code == 200:
            return ret.json()
        return None

    def report_fitness(self, population_id:str, fitness_list:list, generation:int):
        url = self.provider + '/api/v1/population/fitness/'     
        body = {'id': population_id, 'generation': generation, 'fitness': fitness_list}
        print(body)
        ret = requests.post(url, json=body)
        if ret.status_code == 201:
            return True
        return False

    def evolve(self, population_id:str):
        url = self.provider + '/api/v1/population/generation/'
        body = {'id': population_id, 'pmu': 0.3, 'pcx': 0.9, 'elitist': True}
        ret = requests.post(url, json=body)
        if ret.status_code == 201:
            return True
        return False

class AI(object):
    def __init__(self, ann_id:str, inputs:int, w:list, outputs_types:list):
        self.fitness = None
        self.ann_id  = ann_id
        self.brain   = Network(inputs,w, outputs_types)
    
    def dump(self):
        print( {'ann_id': self.ann_id, 'fitness': self.fitness})
        return {'ann_id': self.ann_id, 'fitness': self.fitness}
        

class RemoteAG(object):
    
    def __init__(self, provider:str, population_id:str=''):
        self.provider = ServiceLayer(provider)
        if population_id == '':
            self.population_id = self.provider.new_population()['id']
        else:
            self.population_id = population_id
        
        self.update()
       
    def update(self):
        population = self.provider.get_population(self.population_id)

        self.generation = population['generation']
        self.population = []
        for pop in population['ANNs']:
            self.population.append(AI(pop['ann_id'], pop['topology']['inputs'], pop['topology']['layers'], pop['topology']['outputs_types']))


    def report_fitness(self, fitness_report=None):
        if fitness_report is None:
            fitness = []
            for ind in self.population:
                fitness.append(ind.dump())
        else:
            fitness = fitness_report
        return self.provider.report_fitness(self.population_id, fitness, self.generation)

    def evolve(self):
        return self.provider.evolve(self.population_id)


if __name__ == '__main__':
    from multiflappy import Game

    ag = RemoteAG('https://sssc-backend.cexar.io/')

    generations = 0
    while generations < 20:
        ind = 0
        game = Game(ag.population)
        report = game.start()
        print('Respuesta: ', report)
        print('Reporting Fitness: ', ag.report_fitness(report))
        #quit()
        print('Evolving: ', ag.evolve())
        print(ag.update())

#print(ag.population_id)