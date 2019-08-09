import abc

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


