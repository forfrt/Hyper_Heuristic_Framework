"""\
------------------------------------------------------------
USE: python <PROGNAME> (options)
OPTIONS:
    -h : print this help message
    -b BENCHMARK : the benchmark to be tested on (Benchmark in {OneMax, Cliff, Jump, default: OneMax}
------------------------------------------------------------\
"""

from Hyper_Heuristics.LeadingOne import *
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

    def __init__(self, acceptors, probabilities, benchmark, max_step=-1):
        self.acceptors=acceptors
        self.probabilities=probabilities
        self.benchmark=benchmark
        self.num_step=0
        self.acceptor_steps={i:0 for i in self.acceptors}
        self.acceptor_accepts={i:0 for i in self.acceptors}

        self.max_step=max_step
        self.max_goal=0

    def set_benchmark(self, benchmark):
        self.benchmark=benchmark
        self.num_step=0
        self.acceptor_steps={i:0 for i in self.acceptors}
        self.acceptor_accepts={i:0 for i in self.acceptors}

    def step(self):
        acceptor=choices(self.acceptors, weights=self.probabilities, k=1)[0]
        is_accept, steps, goal_after=acceptor.accept(self.benchmark)
        self.num_step+=steps
        self.acceptor_steps[acceptor]+=steps
        self.acceptor_accepts[acceptor]+=steps if is_accept else 0

        if is_accept:
            if self.max_goal<goal_after:
                self.max_goal=goal_after

        if self.num_step%100==0:
            print("current solution at step {} is: {}".format(self.num_step, self.max_goal))



    def optimize(self):
        self.max_goal=self.benchmark.goal(self.benchmark.current_solution)
        while not self.benchmark.reach_go():
            if self.max_step!=-1 and self.num_step>=self.max_step:
                break

            logging.debug("current solution at step {} is: {}".format(self.num_step, self.benchmark._current_solution))
            self.step()


    def stat(self):
        logging.info("totoal number of steps:{}".format(self.num_step))
        logging.info("steps by each acceptors is:{}".format(self.acceptor_steps))
        logging.info("accepts by each acceptors is:{}".format(self.acceptor_accepts))
        logging.info("max_goal ever achieved is {}".format(self.max_goal))


