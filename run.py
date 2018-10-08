from GA_tool import population

# custom variables ####################
# n_generation: the number of generation (evolution)
# population_size: the number of chronosomes in one population
# match_times: the number of matching with oppenent to evaluate the strategy
# init_rand: randomize initial history or not. ('000000')
# prob_cross: the probability of operating crossover
# prob_mutate: the probability of operating mutate
# strategy_type: select strategy type 0 to 6.
# opp_strategy: oppenent's strategy
########################################

n_generation = 50
population_size = 20
match_times = 40
init_rand = False

prob_cross = .5
prob_mutate = .05

strategy_type = 0
strategy_list = ['AllD', 'AllC', 'Trigger', 'CDCD', 'CCD', 'Random', 'Tit-For-Tat']
            
if __name__ == '__main__':
    fitness_list = []
    p = population(population_size, prob_cross)
    fitness = 0
    opp_fitness = 0
    pt = population(1, match_times, init_rand, prob_cross)
    for x in range(n_generation):
        p.generation(strategy_type)
    pt.glist[0] = p.bestGene
    # select one best gene in population and evaluate again
    pt.evaluate(strategy_type)
    fitness += pt.bestFitness
    opp_fitness += pt.oppFitness
    print('best chromosome from GA:', pt.bestChromosome)
    print('for strategy', strategy_list[strategy_type], ', maximum fitness:', pt.bestFitness,'/', pt.oppFitness)
