import abc

class Benchmark(abc.ABC):

    @abc.abstractmethod
    def goal(self, solution):
        pass

    @abc.abstractmethod
    def mutate(self):
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

    @staticmethod
    def benchmark_factory(class_name, *args):
        print(all_subclasses(Benchmark))
        for cls in all_subclasses(Benchmark):
            if cls.__name__.lower()==class_name.lower():
                return cls(*args)

        return None

def all_subclasses(cls):
    return set(cls.__subclasses__()).\
        union([s for c in cls.__subclasses__() for s in all_subclasses(c)])

