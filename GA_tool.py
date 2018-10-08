import random, copy
import numpy as np

# gene class contains gdata (chromosome), history (index of chromosome) and fitness of that
class gene:
    def __init__(self, init_rand=True):
        self.gdata = "{0:064b}".format(random.randint(0, 2**64-1))
        
        # assigning initial history as random for reducing the effects of bias
        if init_rand:
            self.history = "{0:06b}".format(0, 2**6-1)
        else:
            self.history = "{0:06b}".format(0)
        self.fitness = 0
        
    # function that matching for single oppenent's input (0 or 1). 
    # update the fitness of each gene, history indexes (2 right-shift opperation),
    # and return the selection of itself and oppenent's (to accumulate them to history)
    def match(self, oppenent):
        selection = self.gdata[int(self.history, 2)]
        self.fitness += judgement(selection, oppenent)
        self.history = self.history[2::] + selection + oppenent
        return selection + oppenent
    
    # set the fitness of gene as 0. no use of this function, the gene which lived long time would have
    # more fitness than the newbie gene at every generation.
    # in the environment, no evolution occured.
    def clean(self):
        self.fitness = 0
        
# population class that have several genes as a list (whose size is defined at first).
# glist: size of gene (encoding size)
# plist: size of population
# tmpglist: temporary glist which includes generated and origianl genes
# prob_cross: probability of crossover operation
# prob_mutate: probability of mutation operation
# match_times: how many times the gene matches for each strategy at one generation
# bestFitness: maximum fitness value of gene contained in glist
# oppFitness: oppenent's fitness value for comparing the genes
# bestGene: class gene which have maximum fitness
# bestChromosome: gdata of bestGene
# strategy_list: the strategies which we will test
class population:
    def __init__(self, size=20, match_times=40, init_rand=True, prob_cross=.1, prob_mutate=.05):
        self.glist = list()
        for _ in range(size):
            self.glist.append(gene(init_rand))
        self.gsize = 64
        self.psize = size
        self.tmpglist = list()
        
        self.prob_cross = prob_cross
        self.prob_mutate = prob_mutate
        self.match_times = match_times
        
        self.bestFitness = 0
        self.oppFitness = 0
        self.bestGene = ''
        self.bestChromosome = ''
        
        self.strategy_list = ['AllD', 'Trigger', 'CDCD', 'CCD', 'Random', 'Tit-For-Tat']
        
    # nested crossover function that has two index inputs which inform 
    # the n-th gene and m-th gene that would crossover.
    # only newly generated gene appended in temporary gene list
    def _crossover(self, cidx1, cidx2):
        randIdx = random.randint(0, self.gsize-1)
        target1 = copy.deepcopy(self.glist[cidx1])
        target2 = copy.deepcopy(self.glist[cidx2])
        new_c1 = target1.gdata[0:randIdx] + target2.gdata[randIdx::]
        new_c2 = target2.gdata[0:randIdx] + target1.gdata[randIdx::]
        new_chromosome1 = gene()
        new_chromosome2 = gene()
        new_chromosome1.gdata = new_c1
        new_chromosome2.gdata = new_c2
        
        self.tmpglist.append(new_chromosome1)
        self.tmpglist.append(new_chromosome2)
        #self.tmpglist.append(self.glist[cidx1])
        #self.tmpglist.append(self.glist[cidx2])
        
    # nested mutation function that has one index input which informs
    # the n-th gene that would mutate.
    # only newly generated gene appended in temporary gene list        
    def _mutation(self, cidx):
        randIdx = random.randint(0, self.gsize-1)
        target = copy.deepcopy(self.glist[cidx])
        new_c = list(target.gdata)
        if new_c[randIdx] == '0':
            new_c[randIdx] = '1'
        else:
            new_c[randIdx] = '0'
        new_c = ''.join(new_c)        
        new_chromosome = gene()
        new_chromosome.gdata = new_c        
        self.tmpglist.append(new_chromosome)
        #self.tmpglist.append(self.glist[cidx])
    
    # crossover function for entire population by selecting random two indexes which are not same.
    # whenever random.random() is smaller than prob_cross, crossover activated.
    def crossover(self):
        idxList = np.arange(self.psize)
        np.random.shuffle(idxList)
        idx1 = idxList[0:int(len(idxList)/2)]
        idx2 = idxList[int(len(idxList)/2)::]
        for i in range(len(idx1)):
            if random.random() < self.prob_cross:
                self._crossover(idx1[i], idx2[i])
            #else:
                #self.tmpglist.append(self.glist[idx1[i]])
                #self.tmpglist.append(self.glist[idx2[i]])
    
    # mutation function for entire population by selecting every indexes in glist.
    # whenever random.random() is smaller than prob_mutate, mutation activated.
    def mutation(self):
        for i in range(self.psize):
            if random.random() < self.prob_mutate:
                self._mutation(i)
            #else:
                #self.tmpglist.append(self.glist[i])
    
    # the function that evaluate the genes in tmpglist or glist.
    # for every genes in tmpglist (or glist), get the results, update the history, and undate the fitness
    # the end of the function, glist is only the tmpglist whose size is population size,
    # reversly sorted by the fitness values.
    def evaluate(self, types):
        if self.tmpglist == []:
            target = self.glist
        else:
            target = self.tmpglist
        self.strategy = strategy(len(target))
        for i, gene in enumerate(target):
            for _ in range(self.match_times):
                result = gene.match(self.strategy.selection(types))
                self.strategy.opp_history += result[0]
                self.strategy.history += result[-1]
                self.strategy.fitness[i] = judgement(result[-1], result[0])
                self.strategy.fitness_sum += self.strategy.fitness[i]
        self.glist = copy.deepcopy(sorted(target, key=lambda x: x.fitness, reverse=True))[0:self.psize]
        #print([a.fitness for a in self.glist])
        self.bestFitness = self.glist[0].fitness
        if len(target) == 1:
            self.oppFitness = int(self.strategy.fitness_sum)
        else:
            self.oppFitness = self.strategy.fitness_sum / len(target)
        self.bestGene = self.glist[0]
        self.bestChromosome = self.glist[0].gdata
        self.tmpglist = list()
            
    # operated one generation by genetic algorithms.
    # crossover -> mutation -> (appending original genes on temporary list) -> evaluate
    # after generation, fitness of gene and oppenents are cleaned.
    def generation(self, types):
        self.crossover()
        self.mutation()
        self.tmpglist += self.glist
        self.evaluate(types)        
        self.clean_fitness()
        self.strategy.clean_fitness()
    
    # cleaning function for population level
    def clean_fitness(self):
        for gene in self.glist:
            gene.clean()
