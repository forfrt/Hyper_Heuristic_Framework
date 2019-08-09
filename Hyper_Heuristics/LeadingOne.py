
import abc
from random import choices
from numpy.random import randint

from Hyper_Heuristics.Benchmark import Benchmark


class LeadingOne(Benchmark, abc.ABC):

    def __init__(self, probability, n):
        self._n=n
        self._current_mutation=None
        self.current_solution=choices([0, 1], weights=[1, probability], k=n)
        print("initial bitstring is:", self.current_solution)

    @abc.abstractmethod
    def goal(self, solution):
        pass

    # flip-one
    def mutate(self):
        goal_before=self.goal(self._current_solution)
        self.current_mutation=randint(0, self._n, size=1)[0]

        temp_solution=self.current_solution.copy()
        temp_solution[self.current_mutation]^=1
        goal_after=self.goal(temp_solution)

        mutated_bit=temp_solution[self.current_mutation]

        return self.current_mutation, mutated_bit, goal_before, goal_after

    def apply(self):
        self.current_solution[self.current_mutation]^=1

    def reach_go(self):
        return True if self.current_solution.count(1)==self._n else False

    @property
    def current_solution(self):
        return self._current_solution

    @current_solution.setter
    def current_solution(self, current_solution):
        self._current_solution=current_solution

    @property
    def current_mutation(self):
        return self._current_mutation

    @current_mutation.setter
    def current_mutation(self, current_mutation):
        self._current_mutation=current_mutation

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

