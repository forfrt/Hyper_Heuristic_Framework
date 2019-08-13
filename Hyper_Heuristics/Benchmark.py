import abc

class Benchmark(abc.ABC):

    @abc.abstractmethod
    def goal(self, solution):
        pass

    @abc.abstractmethod
    def mutates(self):
        pass

    @abc.abstractmethod
    def apply(self, mutations):
        pass

    @abc.abstractmethod
    def reach_go(self):
        pass

    @property
    def current_solution(self):
        return self._current_solution

    @current_solution.setter
    def current_solution(self, current_solution):
        self._current_solution=current_solution

    # @property
    # def current_mutation(self):
    #     return self._current_mutation
    #
    # @current_mutation.setter
    # def current_mutation(self, current_mutation):
    #     self._current_mutation=current_mutation


