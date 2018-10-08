import numpy as np

# strategy types
# 1. AllD (All Defect): always return 1.
# 2. AllC (All Cooperate): always return 0.
# 3. Trigger: start with cooperate (0), then start defecting if oppenent defects.
# 4. CDCD (Cooperate-Defect-Cooperate-Defect): return 0 and 1 alternately.
# 5. CCD (Cooperate-Cooperate-Defect): return 0, 0, and 1 recursively.
# 6. Random: choose random 0 or 1 for 50% of probability.
# 7. Tif-For-Tat: Cooperate in first turn, and trace oppenent's action.

class strategy:
    def __init__(self, size, types):
        self.history = ''
        self.opp_history = ''
        self.ssize = size
        self.fitness = np.zeros(self.ssize)
        self.fitness_sum = 0
        self.types = types
    def selection(self):
        if self.types == 'AD' or self.types == 0:
            return self.AllD()            
        elif self.types == 'AC' or self.types == 1:
            return self.AllC()
        elif self.types == 'Tr' or self.types == 2:
            return self.trigger()
        elif self.types == 'CDCD' or self.types == 3:
            return self.CDCD()
        elif self.types == 'CCD' or self.types == 4:
            return self.CCD()
        elif self.types == 'R' or self.types == 5:
            return self.random()
        elif self.types == 'TFT' or self.types == 6:
            return self.tit_for_tat()
    def AllD(self):
        return '1'
    def AllC(self):
        return '0'
    def CDCD(self):
        if len(self.history) == 0:
            return '0'
        if len(self.history) % 2 == 0:
            return '0'
        else:
            return '1'
    def CCD(self):
        if len(self.history) == 0:
            return '0'
        if self.history[-2::] == '00':
            return '1'
        else:
            return '0'
    def random(self):
        return str(random.randint(0,1))
    def trigger(self):
        if len(self.history) == 0:
            answer = '0'
        if '1' in self.opp_history:
            answer = '1'
        else:
            answer = '0'
        return answer
    def tit_for_tat(self):
        if len(self.history) == 0:
            return '0'
        else:
            return self.opp_history[-1]
    def clean_fitness(self):
        self.history = []
        self.opp_history = []
        self.fitness = np.zeros(self.ssize)
        self.fitness_sum = 0
