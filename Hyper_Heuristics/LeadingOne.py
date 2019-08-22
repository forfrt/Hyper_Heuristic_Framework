
import abc
from random import choices, sample

from Hyper_Heuristics.Benchmark import Benchmark


class LeadingOne(Benchmark, abc.ABC):

    def __init__(self, n, probability=1):
        self._n=n
        self.current_solution=choices([0, 1], weights=[1, probability], k=n)
        print("initial bitstring is:", self.current_solution)

    @abc.abstractmethod
    def goal(self, solution):
        pass

    def mutate(self, mutate_fun_name, *args):
        try:
            fn=getattr(self, mutate_fun_name)
            if callable(fn):
                return fn(*args)
            else:
                temp_fn=getattr(self, self.mutates()[0][0])
                return temp_fn(*self.mutates()[0][1])
        except AttributeError:
            raise NotImplementedError(
                "Class `{}` does not implement `{}`".format(self.__class__.__name__, mutate_fun_name))

    # flip-one
    def mutates(self):
        # return [self.flip_n(1)]
        return [("flip_n", [1])]

    def flip_n(self, n):
        # Multiprocessing need pickle to send to its worker-processes but Nested function cannot be pickled

        # def flip():
        mutations=sample(range(0, self._n), n)

        temp_solution=self.current_solution.copy()
        for mutation in mutations:
            temp_solution[mutation]^=1
        goal_after=self.goal(temp_solution)

        mutated_bits=[temp_solution[i] for i in mutations]

        return mutations, mutated_bits, goal_after

        # return flip


    def apply(self, mutations):
        for mutation in mutations:
            self.current_solution[mutation]^=1

    def reach_go(self):
        return True if self.current_solution.count(1)==self._n else False


#==============================================================================
# OneMax Benchmark

class OneMax(LeadingOne):

    def __init__(self, n, probability=1):
        n=int(n)
        probability=float(probability)
        super().__init__(n, probability)

    def goal(self, solution):
        return solution.count(1)



#==============================================================================
# Cliff Benchmark

class Cliff(LeadingOne):

    def __init__(self, n, d, probability=1):
        super().__init__(n, probability)
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

    def __init__(self, n, m, probability=1):
        super().__init__(n, probability)
        self._m=m

    def goal(self, solution):
        count_1=solution.count(1)
        if count_1<=(self._n-self._m):
            return self._m+count_1
        elif count_1==self._n:
            return self._n+self._m
        else:
            return self._n-count_1

