"""\
------------------------------------------------------------
USE: python <PROGNAME> (options)
OPTIONS:
    -h : print this help message
    -b BENCHMARK : the benchmark to be tested on (Benchmark in {OneMax, Cliff, Jump, default: OneMax}
------------------------------------------------------------\
"""

from random import choices
from Hyper_Heuristics.Acceptor import *
from Hyper_Heuristics.Benchmark import *
import sys, getopt, logging

#==============================================================================
# Command line processing

class CommandLine:
    def __init__(self):
        opts, args = getopt.getopt(sys.argv[1:], 'hs:')
        opts = dict(opts)
        self.exit = True

        if '-h' in opts:
            self.printHelp()
            return

        if '-s' in opts:
            if opts['-s'] in ('char', 'word'):
                self.token = opts['-s']
            else:
                warning = (
                    "*** ERROR: symbol for Huffman coding (opt: -s TOKEN)! ***\n"
                    "    -- value (%s) not recognised!\n"
                    "    -- must be one of: char / word "
                    )  % (opts['-s'])
                print(warning, file=sys.stderr)
                self.printHelp()
                return
        else:
            self.token = 'char'

        if len(args) == 1:
            self.infile = args[0]
        else:
            print('\n*** ERROR: must specify precisely 1 arg files (infile) ***', file=sys.stderr)
            self.printHelp()

        self.exit = False

    def printHelp(self):
        progname = sys.argv[0]
        progname = progname.split('/')[-1] # strip off extended path
        help = __doc__.replace('<PROGNAME>', progname, 1)
        print(help, file=sys.stderr)


class HH:

    def __init__(self, acceptors, probabilities, benchmark):
        self.acceptors=acceptors
        self.probabilities=probabilities
        self.benchmark=benchmark
        self.num_step=0
        self.acceptor_steps={i:0 for i in self.acceptors}
        self.acceptor_accepts={i:0 for i in self.acceptors}

    def step(self):
        acceptor=choices(self.acceptors, weights=self.probabilities, k=1)[0]
        mutation, goal_b, goal_a=self.benchmark.mutate()

        mutated_bit=self.benchmark.current_solution[mutation]

        is_accept=acceptor.accept(goal_b, goal_a)

        self.num_step+=1
        self.acceptor_steps[acceptor]+=1
        if is_accept:
            self.benchmark.apply()
            self.acceptor_accepts[acceptor]+=1

        logging.debug("choosen acceptor: {} is accepted: {} with mutation {} on {}, goal_b: {}, goal_a: {}".
              format(str(acceptor), is_accept, mutation, mutated_bit, goal_b, goal_a))

    def optimize(self):
        while not self.benchmark.reach_go():
            logging.debug("current solution at step {} is {}:".format(self.num_step, self.benchmark._current_solution))
            self.step()

    def stat(self):
        print("steps by each acceptors is:", self.acceptor_steps)
        print("accepts by each acceptors is:", self.acceptor_accepts)


def main():
    am=AM()
    oi=OI()

    logging.basicConfig(filename="hh.log", level=logging.DEBUG,
                        format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

    init_bitstring=choices([0, 1], weights=[5, 1], k=10)
    print("initial bitstring is:", init_bitstring)

    # oneMax=OneMax(init_bitstring)
    # hh_one=HH([am, oi], [1, 10], oneMax)
    # hh_one.optimize()
    # hh_one.stat()

    # cliff=Cliff(init_bitstring, d=4)
    # hh_cliff=HH([am, oi], [1, 1], cliff)
    # hh_cliff.optimize()
    # hh_cliff.stat()

    jump=Jump(init_bitstring, m=4)
    hh_jump=HH([am, oi], [1, 1], jump)
    hh_jump.optimize()
    hh_jump.stat()


main()