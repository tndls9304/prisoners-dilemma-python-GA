from GA_utils import population
from strategy import strategy

# custom variables ####################
# n_generation: the number of generation (evolution)
# population_size: the number of chronosomes in one population
# match_times: the number of matching with oppenent to evaluate the strategy
# prob_cross: the probability of operating crossover
# prob_mutate: the probability of operating mutate
# opp_strategy: oppenent's strategy
########################################

n_generation = 50
population_size = 20
match_times = 40

prob_cross = .5
prob_mutate = .05

strategy_list = ['AllD', 'AllC', 'Trigger', 'CDCD', 'CCD', 'Random', 'Tit-For-Tat']

opp_startegy = strategy(0)

def judgement(my_selection, oppenent):
    cooperate = 3
    defected = 0
    punished = 1
    defecting = 5
    if my_selection == '0':
        if oppenent == my_selection:
            return cooperate
        else:
            return defected
    elif my_selection == '1':
        if oppenent == my_selection:
            return punished
        else:
            return defecting
            
if __name__ == '__main__':
    fitness_list = []
    for _ in range(10):
      for s in settings:
          #print('settings for ', s, '\n')
          p = population(s[0], prob_cross=k/10)
          fitness = 0
          opp_fitness = 0
          for i in range(len(strategy_list)):
              if i == 1:
                  pt = population(1, match_times=s[1], init_rand=False, prob_cross=k/10)
              else:
                  pt = population(1, prob_cross=k/10)
              for x in range(s[2]):
                  p.generation(i)
              pt.glist[0] = p.bestGene
              pt.evaluate(i)
              fitness += pt.bestFitness
              opp_fitness += pt.oppFitness
              #print('best chromosome from GA:', pt.bestChromosome)
              #print('for strategy', strategy_list[i], ', maximum fitness:', pt.bestFitness,'/', pt.oppFitness)
      fitness_list.append(fitness / opp_fitness)
    print(np.average(fitness_list))
