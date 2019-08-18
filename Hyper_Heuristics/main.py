"""\
------------------------------------------------------------
USE: python <PROGNAME> (options)
OPTIONS:
    -b --benchmark BENCHMARK : the benchmark to be tested on (Benchmark in {OneMax, Cliff, Jump, Sat default: OneMax}
    -s --show : show the statistic bar chart based on pervious data
    --acceptors : a list of acceptors chosen to be selected
    --acceptor_probs : probabilities of given acceptors
    --sat_files : CNF files if SAT benchmark is selected
    --num_instance : number of instance to be tested
    --num_run : number of run for each problem instance
    --log_file : logging file
    --dump_file : file that store the json.dumps() result
    --max_mutation : maximum number of mutation
------------------------------------------------------------\
"""
import logging, glob, json, argparse, pathlib
import matplotlib.pyplot as plt
from math import ceil
import numpy as np

from Hyper_Heuristics.HH import *
from Hyper_Heuristics.Satlib import *
from Hyper_Heuristics.Acceptor import *
from Hyper_Heuristics.LeadingOne import *

#==============================================================================
# Command line processing

def proc_cmd():
    cli=argparse.ArgumentParser()
    cli.add_argument("-b", "--benchmark",
                     help="BENCHMARK : the benchmark to be tested on (Benchmark in {OneMax, Cliff, Jump, Sat default: Sat}")
    cli.add_argument("-s", "--show", action="store_true", help="show the statistic bar chart based on pervious data")
    cli.add_argument("--sat_files", default="./sat/", help="CNF files if SAT benchmark is selected")
    cli.add_argument("--acceptors", nargs="+", default=["am", "oi"], help="a list of acceptors chosen to be selected")
    cli.add_argument("--acceptor_probs", nargs="+", type=float, default=[1, 1], help="probabilities of given acceptors")
    cli.add_argument("--max_mutation", type=int, default="200000", help="maximum number of mutation")
    cli.add_argument("--num_instance", type=int, default=100, help="number of instance to be tested")
    cli.add_argument("--num_run", type=int, default=100, help="number of run for each problem instance")
    cli.add_argument("--log_file", default="hh.log", help="logging file")
    cli.add_argument("--dump_file", default="hh_data.dump", help="file that store the json.dumps() result")

    args=cli.parse_args()


    return cli, args

def test_leadingone():
    oneMax=OneMax(n=100, probability=0.2)
    hh_one=HH(["am", "oi"], [0, 1], oneMax)
    hh_one.optimize()
    hh_one.stat()

    # cliff=Cliff(probability=0.2, n=100, d=25)
    # hh_cliff=HH([am, oi], [0.01, 0.99], cliff)
    # hh_cliff.optimize()
    # hh_cliff.stat()
    #
    # jump=Jump(probability=0.2, n=100, m=25)
    # hh_jump=HH([am, oi], [1, 1], jump)
    # hh_jump.optimize()
    # hh_jump.stat()


def main():

    # test_leadingone()
    cli, args=proc_cmd()
    if args.benchmark.lower() in ["onemax", "cliff", "jump", "sat"]:
        if args.benchmark.lower()=='sat':
            if args.sat_files:
                p=pathlib.Path(args.sat_files)
                if not (p.exists() and p.is_dir()):

                    warning = ( "*** ERROR: directory for sat files (opt: --sat_files SAT_DIR default: ./sat)! ***\n"
                                "    -- path (%s) not exists!\n"
                                "    -- must be a existent directory"
                                )  % (args.sat_files)
                    print(warning, file=sys.stderr)
                    cli.print_help()
                    sys.exit()
    else:
        warning = (
                      "*** ERROR: benchmark for Hyper-Heuristic (opt: --benchmark BENCHMARK default: Sat)! ***\n"
                      "    -- value (%s) not recognised!\n"
                      "    -- must be one of: OneMax / Cliff / Jump / Sat "
                  )  % (args.benchmark)
        print(warning, file=sys.stderr)
        cli.print_help()
        sys.exit()


    logging.basicConfig(filename=args.log_file, level=logging.INFO,
                        format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

    logging.info(args)
    # max_mutate=1600000
    # num_run=10
    # num_instance=20
    num_per_subp=5
    # dump_file='uf20_2'

    hh_sat=HH(args.acceptors, args.acceptor_probs, None, args.max_mutation) # 2/n
    uf_num, uf_goal, uf_mutate=opt_sat(args.sat_files, hh_sat, args.num_instance, args.num_run)

    dump_to_file(args.dump_file, uf_num=uf_num, uf_goal=uf_goal, uf_mutate=uf_mutate)

    uf_num, uf_goal, uf_mutate=loads_from_file(args.dump_file, 3)

    if args.show:
        average_goal, average_mutation=draw_bar_charts(num_per_subp, uf_num, uf_goal, uf_mutate)
        dump_to_file(args.dump_file, average_goal=average_goal, average_mutation=average_mutation)

def dump_to_file(filename, **kwargs):
    with open(filename, 'a') as f:
        for k, v in kwargs.items():
            f.write(k+'\n')
            f.write(json.dumps(v)+'\n')

def loads_from_file(filename, num_value):
    res=list()
    with open(filename, 'r') as f:
        tmp_value=None
        for i in range(num_value):
            f.readline()
            res.append(json.loads(f.readline()))

    return tuple(res)

def opt_sat(dir_name, hh_sat, num_instance, num_run):

    uf_li=list(pathlib.Path(dir_name).glob("**/*.cnf"))
    uf_num=[[0]*num_instance for _ in range(2)]
    uf_mutate=[[0]*num_instance for _ in range(2)]
    uf_goal=[[0]*num_instance for _ in range(2)]

    for instance_id in range(num_instance):
        logging.info("======NEXT INSTANCE:{}======".format(instance_id))

        sat=Sat(str(uf_li[instance_id]))
        sat.print_inner_var()

        for i in range(num_run):

            logging.info("------NEXT RUN:{}------".format(i))
            sat.reset_solution()
            hh_sat.reset_benchmark(sat)
            hh_sat.optimize()
            hh_sat.stat()

            # find global optima within max_mutate
            if hh_sat.max_goal==sat.num_cla:
                uf_num[0][instance_id]+=1
                uf_goal[0][instance_id]+=sat.num_cla
                uf_mutate[0][instance_id]+=hh_sat.num_mutate
            # didn't find global optima within max_mutate
            else:
                uf_num[1][instance_id]+=1
                uf_goal[1][instance_id]+=hh_sat.max_goal
                uf_mutate[1][instance_id]+=hh_sat.max_mutate

    return uf_num, uf_goal, uf_mutate


def draw_bar_charts(inst_per_subp, uf_num, uf_goal, uf_mutate):

    width=0.35

    average_goal=list()
    average_mutation=list()

    fig=plt.figure()
    fig.suptitle("Average goal/step for each instance")
    fig, ax_lst=plt.subplots(ceil(len(uf_num[0])/inst_per_subp), 3)

    for instance_subp_id in range(0, len(uf_num[0]), inst_per_subp):
        x_ind=np.arange(instance_subp_id, instance_subp_id+inst_per_subp)

        time_glo=ax_lst[int(instance_subp_id/inst_per_subp)][0]\
            .bar(x_ind-width/2, uf_num[0][instance_subp_id:instance_subp_id+inst_per_subp], width,
                 label="Time for instances that achieved global optima".format())

        time_loc=ax_lst[int(instance_subp_id/inst_per_subp)][0]\
            .bar(x_ind+width/2, uf_num[1][instance_subp_id:instance_subp_id+inst_per_subp], width,
                 label="Time for instances that didn't achieved global optima".format())

        autolabel(ax_lst[int(instance_subp_id/inst_per_subp)][0], time_glo, "left")
        autolabel(ax_lst[int(instance_subp_id/inst_per_subp)][0], time_loc, "right")

        average_goal_subp=list()
        average_mutation_subp=list()

        for id in range(inst_per_subp):
            instance_id=instance_subp_id+id

            print("The times for instance {} that achieved global optima is {}, times that didn't achieved is {}"
                .format(instance_id, uf_num[0][instance_id], uf_num[1][instance_id]))

            if uf_num[0][instance_id]!=0:
                print("The average mutation to achieve global optima {} is {}".
                    format(uf_goal[0][instance_id]/uf_num[0][instance_id], uf_mutate[0][instance_id]/uf_num[0][instance_id]))
                average_mutation_subp.append(uf_mutate[0][instance_id]/uf_num[0][instance_id])
            else:
                average_mutation_subp.append(0)

            if uf_num[1][instance_id]!=0:
                print("The average maximum goal achieved within {} steps is {}".
                    format(uf_mutate[1][instance_id]/uf_num[1][instance_id], uf_goal[1][instance_id]/uf_num[1][instance_id]))
                average_goal_subp.append(uf_goal[1][instance_id]/uf_num[1][instance_id])
            else:
                average_goal_subp.append(0)

        ax_lst[int(instance_subp_id/inst_per_subp), 1].bar(x_ind,
                                                 np.array(average_goal_subp), width,
                                                 label="")
        ax_lst[int(instance_subp_id/inst_per_subp), 2].bar(x_ind,
                                                 np.array(average_mutation_subp), width,
                                                 label="")

        average_goal.extend(average_goal_subp)
        average_mutation.extend(average_mutation_subp)

    fig.show()

    return average_goal, average_mutation


def autolabel(ax, rects, xpos='center'):
    """
    Attach a text label above each bar in *rects*, displaying its height.

    *xpos* indicates which side to place the text w.r.t. the center of
    the bar. It can be one of the following {'center', 'right', 'left'}.
    """

    ha = {'center': 'center', 'right': 'left', 'left': 'right'}
    offset = {'center': 0, 'right': 1, 'left': -1}

    for rect in rects:
        height = rect.get_height()
        ax.annotate('{}'.format(height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(offset[xpos]*3, 3),  # use 3 points offset
                    textcoords="offset points",  # in both directions
                    ha=ha[xpos], va='bottom')


if __name__ == '__main__':
    main()

