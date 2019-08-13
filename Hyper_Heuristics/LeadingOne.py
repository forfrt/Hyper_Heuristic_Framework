
import abc
from random import choices, sample

from Hyper_Heuristics.Benchmark import Benchmark


class LeadingOne(Benchmark, abc.ABC):

    def __init__(self, probability, n):
        self._n=n
        self.current_solution=choices([0, 1], weights=[1, probability], k=n)
        print("initial bitstring is:", self.current_solution)

    @abc.abstractmethod
    def goal(self, solution):
        pass

    # flip-one
    def mutates(self):
        return [self.flip_n(1)]

    def flip_n(self, n):

        def flip():
            # goal_before=self.goal(self._current_solution)
            mutations=sample(range(0, self._n), n)

            temp_solution=self.current_solution.copy()
            for mutation in mutations:
                temp_solution[mutation]^=1
            goal_after=self.goal(temp_solution)

            mutated_bits=[temp_solution[i] for i in mutations]

            return mutations, mutated_bits, goal_after

        return flip


    def apply(self, mutations):
        for mutation in mutations:
            self.current_solution[mutation]^=1

    def reach_go(self):
        return True if self.current_solution.count(1)==self._n else False


#==============================================================================
# OneMax Benchmark

class OneMax(LeadingOne):

    def __init__(self, probability, n):
        super().__init__(probability, n)

    def goal(self, solution):
        return solution.count(1)



#==============================================================================
# Cliff Benchmark

class Cliff(LeadingOne):

    def __init__(self, probability, n, d):
        super().__init__(probability, n)
        self._d=d

    def goal(self, solution):
        count_1=solution.count(1)
        if count_1<=self._n-self._d:
            return count_1
        else:
            return count_1-self._d+0.5


#==============================================================================
# Jump Benchmark

class Jump(LeadingOne):

    def __init__(self, probability, n, m):
        super().__init__(probability, n)
        self._m=m

    def goal(self, solution):
        count_1=solution.count(1)
        if count_1<=(self._n-self._m):
            return self._m+count_1
        elif count_1==self._n:
            return self._n+self._m
        else:
            return self._n-count_1

