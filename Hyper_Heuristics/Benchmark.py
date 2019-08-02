import abc
from numpy.random import randint

class Benchmark(abc.ABC):

    @abc.abstractmethod
    def goal(self, solution):
        pass

    @abc.abstractmethod
    def mutate(self):
        pass

    @abc.abstractmethod
    def apply(self):
        pass

    @abc.abstractmethod
    def reach_go(self):
        pass

    @property
    @abc.abstractmethod
    def current_solution(self):
        pass

    @current_solution.setter
    @abc.abstractmethod
    def current_solution(self, current_solution):
        pass

    @property
    @abc.abstractmethod
    def current_mutation(self):
        pass

    @current_mutation.setter
    @abc.abstractmethod
    def current_mutation(self, current_mutation):
        pass


class LeadingOne(Benchmark, abc.ABC):

    def __init__(self, init_solution):
        self._current_solution=init_solution
        self._current_mutation=None

    def goal(self, solution):
        pass

    # flip-one
    def mutate(self):
        goal_before=self.goal(self._current_solution)
        self._current_mutation=randint(0, len(self._current_solution), size=1)[0]
        temp_solution=self._current_solution.copy()
        temp_solution[self._current_mutation]^=1
        goal_after=self.goal(temp_solution)

        return self._current_mutation, goal_before, goal_after

    def apply(self):
        self._current_solution[self._current_mutation]^=1

    def reach_go(self):
        return True if self._current_solution.count(1)==len(self._current_solution) else False

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

    def __init__(self, init_solution):
        super().__init__(init_solution)

    def goal(self, solution):
        return solution.count(1)



#==============================================================================
# Cliff Benchmark

class Cliff(LeadingOne):

    def __init__(self, init_solution, d):
        super().__init__(init_solution)
        self._d=d

    def goal(self, solution):
        count_1=solution.count(1)
        n=len(self._current_solution)
        if count_1<=n-self._d:
            return count_1
        else:
            return count_1-self._d+0.5


#==============================================================================
# Jump Benchmark

class Jump(LeadingOne):

    def __init__(self, init_solution, m):
        super().__init__(init_solution)
        self._n=len(init_solution)
        self._m=m

    def goal(self, solution):
        count_1=solution.count(1)
        if count_1<=(self._n-self._m):
            return self._m+count_1
        elif count_1==self._n:
            return self._n+self._m
        else:
            return self._n-count_1


