import logging
from Hyper_Heuristics.LeadingOne import *

class GapPath(LeadingOne):

    def __init__(self, n):
        n=int(n)
        self._n=n
        self.current_solution=[0]*n
        self.current_solution[0]=1
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

        logging.info("solution:{} count_0:{}, rid:{}".
                      format(solution, count_0, rid))

        if rid % 3==1:
            return count_0
        else:
            return count_0+2*rid

    def mutates(self):
        return [("flip_n", [1]), ("flip_n", [2])]

    @property
    def current_solution(self):
        return self._current_solution

    @current_solution.setter
    def current_solution(self, current_solution):
        self._current_solution=current_solution


class GGP(GapPath):
    def goal(self, solution):
        pass
