import re, logging
from random import choices
from Hyper_Heuristics.LeadingOne import *

class Sat(LeadingOne):
    def __init__(self, filename):
        self.filename=filename
        self.clas=list()
        self.clas.append(list())

        f=open(filename, "r")
        contents=f.readlines()
        f.close()

        self.proc_contents(contents)


    def proc_contents(self, contents):

        for line in contents:
            if line.startswith('c'):
                continue

            elif line.startswith('p'):
                match= re.match('p\s+cnf\s+(\d+)\s+(\d+)', line)
                if not match:
                    logging.error("The Sat Format maybe wrong: {}"
                                  .format(line))
                    break

                self._n, self.num_cla=int(match.group(1)), int(match.group(2))
                self.current_solution=choices([0, 1], weights=[1, 1], k=self._n)
                logging.debug("num_var:{}, num_cla:{}".format(self._n, self.num_cla))

            else:
                iter=re.finditer("[-]?\d+", line)
                for i in iter:
                    var=int(i.group(0))
                    if var==0:
                        self.clas.append(list())
                        logging.debug("Added a new list into self.clas by {}".format(var))
                    else:
                        self.clas[-1].append(var)
                        logging.debug("Added element into self.clas[-1] by {}".format(var))


    def print_inner_var(self):
        logging.info("num_var:{}, num_cla:{}".format(self._n, self.num_cla))
        logging.info("self.clas:{}, self.vars:{}".format(self.clas, self.current_solution))

    def apply(self):
        self.current_solution[self.current_mutation]^=1

    def goal(self, solution):
        _goal=0
        for cla in self.clas:
            for ele in cla:
                if ele<0:
                    if solution[abs(ele)-1]==0:
                        _goal+=1
                        break
                else:
                    if solution[abs(ele)-1]==1:
                        _goal+=1
                        break

        return _goal

    def reach_go(self):
        return True if self.goal(self.current_solution)==self.num_cla else False

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


