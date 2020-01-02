from LeadingOne import *
from Satlib import *
from GapPath import *
from Acceptor import *

class HH:

    def __init__(self, acceptor_names, probabilities, benchmark, max_mutate=-1):
        self.acceptors=[Acceptor.acceptor_factory(acceptor_name, benchmark) for acceptor_name in acceptor_names]
        self.probabilities=probabilities
        self.benchmark=benchmark

        #! number of mutation
        self.num_mutate=0
        #! time of acceptor get selected
        self.acceptor_sel_time={i:0 for i in self.acceptors}
        #! time of acceptor get accepted
        self.acceptor_acc_time={i:0 for i in self.acceptors}
        #! number of mutation took to reach the global optima
        self.num_mutate_to_max_goal=0

        #! maximum limit of mutation
        self.max_mutate=max_mutate
        #! maximum goal has ever achieved
        self.max_goal=0

    def reset_benchmark(self, benchmark):
        self.benchmark=benchmark
        for acceptor in self.acceptors:
            acceptor.benchmark=benchmark

        self.num_mutate=0
        self.num_mutate_to_max_goal=0
        self.acceptor_sel_time={i:0 for i in self.acceptors}
        self.acceptor_acc_time={i:0 for i in self.acceptors}

        self.max_goal=0

    def step(self):
        acceptor=choices(self.acceptors, weights=self.probabilities, k=1)[0]
        is_accept, num_mutate, goal_after=acceptor.accept()

        self.num_mutate+=num_mutate
        self.acceptor_sel_time[acceptor]+=1
        self.acceptor_acc_time[acceptor]+=1 if is_accept else 0

        if is_accept:
            if self.max_goal<goal_after:
                self.max_goal=goal_after
                self.num_mutate_to_max_goal=self.num_mutate

        if self.num_mutate%1000==0:
           logging.debug("current solution at step {} has max_goal: {}, goal_after:{}".format(self.num_mutate, self.max_goal, goal_after))


    def optimize(self):
        self.max_goal=self.benchmark.goal(self.benchmark.current_solution)
        while not self.benchmark.reach_go():
            if self.max_mutate!=-1 and self.num_mutate>=self.max_mutate:
                break

            self.step()

        logging.info("max goal ever achieved by current solution at step {} is: {}".format(self.num_mutate, self.max_goal))


    def stat(self):
        logging.info("total number of mutate:{}".format(self.num_mutate))
        logging.info("each acceptor is picked for:{}".format(self.acceptor_sel_time))
        logging.info("each acceptor is accepted for:{}".format(self.acceptor_acc_time))
        logging.info("max_goal ever achieved is {}".format(self.max_goal))


