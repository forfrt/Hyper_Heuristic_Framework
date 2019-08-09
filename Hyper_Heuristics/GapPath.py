import logging
from numpy.random import randint
from Hyper_Heuristics.Benchmark import *

class GapPath(Benchmark, abc.ABC):

    def __init__(self, n):
        self.current_solution=[0]*n
        self.current_solution[0]=1
        self._n=n
        self._current_mutation=None
        print("initial bitstring is:", self.current_solution)

    @staticmethod
    def ridge(solution):
        last_1_pos=-1
        count_1=solution.count(1)

        for i in range(len(solution)):
            if solution[i]==1:
                last_1_pos=i
            else:
                break

        logging.debug("solution:{} last_1_pos:{}, count_1:{}".
                      format(solution, last_1_pos, count_1))
        if last_1_pos+1==count_1:
            return last_1_pos+1
        else:
            return 0

    def goal(self, solution):
        count_0=solution.count(0)
        rid=self.ridge(solution)

        logging.debug("solution:{} count_0:{}, rid:{}".
                      format(solution, count_0, rid))

        if rid % 3==1:
            return count_0
        else:
            return count_0+2*rid


    def mutates(self):
        pass

    # flip-one
    def flip_1(self):
        goal_before=self.goal(self.current_solution)
        self.current_mutation=randint(0, len(self.current_solution), size=1)[0]
        temp_solution=self.current_solution.copy()
        temp_solution[self.current_mutation]^=1

        logging.debug("current_solution:{} temp_solution:{}".
                      format(self.current_solution, temp_solution))

        goal_after=self.goal(temp_solution)

        mutated_bit=temp_solution[self.current_mutation]

        return self.current_mutation, mutated_bit, goal_before, goal_after

    # flip-one
    def flip_2(self):
        goal_before=self.goal(self.current_solution)
        self.current_mutation=randint(0, len(self.current_solution), size=1)[0]
        temp_solution=self.current_solution.copy()
        temp_solution[self.current_mutation]^=1

        logging.debug("current_solution:{} temp_solution:{}".
                      format(self.current_solution, temp_solution))

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
