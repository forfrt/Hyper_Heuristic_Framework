"""\
------------------------------------------------------------
USAGE: <PROGNAME> [-h] [-b BENCHMARK] [-s] [--sat_files SAT_FILES]
               [--acceptors ACCEPTORS [ACCEPTORS ...]]
               [--acceptor_probs ACCEPTOR_PROBS [ACCEPTOR_PROBS ...]]
               [--max_mutation MAX_MUTATION]
               [--num_run NUM_RUN] [--log_file LOG_FILE]
               [--dump_file DUMP_FILE]
OPTIONS:
    -s --show : show the statistic bar chart based on pervious data
    --acceptors : a list of acceptors chosen to be selected
    --acceptor_probs : probabilities of given acceptors
    -b --benchmark BENCHMARK : the benchmark to be tested on (Benchmark in {OneMax, Cliff, Jump, Sat default: OneMax}
    --sat_files : CNF files if SAT benchmark is selected
    --num_run : number of run for each problem instance
    --log_file : logging file
    --dump_file : file that store the json.dumps() result
    --max_mutation : maximum number of mutation
------------------------------------------------------------\
"""
import os, re, sys, logging, json, argparse
from statistics import mean, median

import matplotlib.pyplot as plt
from math import ceil
import numpy as np

from HH import *
from Satlib import *
from Acceptor import *
from Benchmark import *

#==============================================================================
# Command line processing

def proc_cmd():
    cli=argparse.ArgumentParser()
    cli.add_argument("-b", "--benchmark",
                     help="BENCHMARK : the benchmark to be tested on (Benchmark in {OneMax, Cliff, Jump, Sat, GapPath default: Sat}")
    cli.add_argument("--benchmark_params", nargs="*", help="benchmark problem parameters if one of [OneMax, Cliff, Jump] is selected")
    cli.add_argument("--sat_files", default="./sat/", help="CNF files if SAT benchmark is selected")
    cli.add_argument("--acceptors", nargs="+", default=["am", "oi"], help="a list of acceptors chosen to be selected")
    cli.add_argument("--acceptor_probs", nargs="+", type=float, default=[1.0, 1.0], help="probabilities of given acceptors")
    cli.add_argument("--max_mutation", type=int, default="200000", help="maximum number of mutation")
    cli.add_argument("--num_run", type=int, default=100, help="number of run for each problem instance")
    cli.add_argument("--log_file", default="hh.log", help="logging file")
    cli.add_argument("--dump_file", default="hh_data.dump", help="file that store the json.dumps() result")
    cli.add_argument("-s", "--show", action="store_true", help="show the statistic bar chart based on pervious data")

    args=cli.parse_args()

    return cli, args

def test_leadingone(args):
    benchmark=Benchmark.benchmark_factory(args.benchmark, *args.benchmark_params)
    hh_lo=HH(args.acceptors, args.acceptor_probs, benchmark, args.max_mutation) # 2/n
    hh_lo.optimize()
    hh_lo.stat()

    # oneMax=OneMax(*args.benchmark_params)
    # hh_one=HH(args.acceptors, args.acceptor_probs, oneMax, args.max_mutation) # 2/n
    # hh_one.optimize()
    # hh_one.stat()

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
    logging.basicConfig(filename=args.log_file, level=logging.INFO,
                        format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    logging.info(args)

    if args.benchmark.lower() in ["onemax", "cliff", "jump", "sat", "gappath"]:
        if args.benchmark.lower()=='sat':
            p, pattern=os.path.split(args.sat_files)
            print(p, pattern)
            if not (os.path.exists(p) and os.path.isdir(p)):
                warning = ( "*** ERROR: directory for sat files (opt: --sat_files SAT_DIR default: ./sat)! ***\n"
                            "    -- path (%s) not exists!\n"
                            "    -- must be a existent directory"
                            )  % (args.sat_files)
                print(warning, file=sys.stderr)
                cli.print_help()
                sys.exit()
            else:
                test_sat(args)
        else:
            test_leadingone(args)
    else:
        warning = (
                      "*** ERROR: benchmark for Hyper-Heuristic (opt: --benchmark BENCHMARK default: Sat)! ***\n"
                      "    -- value (%s) not recognised!\n"
                      "    -- must be one of: OneMax / Cliff / Jump / Sat / GapPath "
                  )  % (args.benchmark)
        print(warning, file=sys.stderr)
        cli.print_help()
        sys.exit()

    if args.dump_file and args.show:
        draw_sat_stat_graph(args.dump_file)


def test_sat(args):

    hh_sat=HH(args.acceptors, args.acceptor_probs, None, args.max_mutation) # 2/n
    uf_li, (uf_mutation, uf_goal), (uf_num, uf_global_ind, uf_mutation_li, uf_goal_li)=\
        opt_sat(args.sat_files, hh_sat, args.num_run)

    dump_to_file(args.dump_file, uf_li=uf_li, uf_mutation=uf_mutation, uf_goal=uf_goal)
    dump_to_file(args.dump_file, uf_num=uf_num, uf_global=uf_global_ind, uf_mutation_li=uf_mutation_li, uf_goal_li=uf_goal_li)

    (average_mutation, average_goal), (median_mutation, median_goal)=calculate_stat(uf_mutation_li, uf_goal_li)

    dump_to_file(args.dump_file, average_mutation=average_mutation, average_goal=average_goal,
                 median_mutation=median_mutation, median_goal=median_goal)

def draw_sat_stat_graph(dump_file):
    num_per_subp=5
    uf_num, average_mutation, average_goal, median_mutation, median_goal=\
        loads_from_file(dump_file, "uf_num", "average_mutation", "average_goal", "median_mutation", "median_goal")
    draw_bar_charts(num_per_subp, uf_num, average_mutation, average_goal, median_mutation, median_goal)

        # average_goal, average_mutation=draw_bar_charts(num_per_subp, uf_num, uf_goal, uf_mutate)


def opt_sat(sat_files, hh_sat, num_run):

    # uf_li=list(pathlib.Path(dir_name).glob("**/*.cnf"))

    p, pattern=os.path.split(sat_files)
    uf_li=[os.path.join(p, x) for x in os.listdir(p) if re.fullmatch(pattern, x)]
    num_instance=len(uf_li)


    uf_mutation=[[0]*num_run for _ in range(num_instance)]
    uf_goal=[[0]*num_run for _ in range(num_instance)]

    uf_num=[[0]*num_instance for _ in range(2)]
    uf_global_ind=[list() for _ in range(2)]
    uf_mutation_li=[[list() for _ in range(num_instance)] for _ in range(2)]
    uf_goal_li=[[list() for _ in range(num_instance)] for _ in range(2)]

    for instance_id in range(num_instance):
        logging.info("======NEXT INSTANCE:{}======".format(instance_id))

        sat=Sat(str(uf_li[instance_id]))
        sat.print_inner_var()

        for run_id in range(num_run):

            logging.info("------NEXT RUN:{}------".format(run_id))
            sat.reset_solution()
            hh_sat.reset_benchmark(sat)
            hh_sat.optimize()
            hh_sat.stat()

            uf_mutation[instance_id][run_id]=hh_sat.num_mutate
            uf_goal[instance_id][run_id]=hh_sat.max_goal

            # find global optima within max_mutate
            if hh_sat.max_goal==sat.num_cla:
                uf_num[0][instance_id]+=1
                uf_global_ind[0].append((instance_id, run_id))
                uf_mutation_li[0][instance_id].append(hh_sat.num_mutate)
                uf_goal_li[0][instance_id].append(hh_sat.max_goal)
            # didn't find global optima within max_mutate
            else:
                uf_num[1][instance_id]+=1
                uf_global_ind[1].append((instance_id, run_id))
                uf_mutation_li[1][instance_id].append(hh_sat.num_mutate)
                uf_goal_li[1][instance_id].append(hh_sat.max_goal)

    return uf_li, (uf_mutation, uf_goal), (uf_num, uf_global_ind, uf_mutation_li, uf_goal_li)

def calculate_stat(uf_mutation_li, uf_goal_li):
    average_goal=[list() for _ in range(2)]
    median_goal=[list() for _ in range(2)]
    average_mutation=[list() for _ in range(2)]
    median_mutation=[list() for _ in range(2)]

    for instance_id in range(len(uf_mutation_li[0])):
        for suc_id in range(2):
            if uf_mutation_li[suc_id][instance_id]:
                average_mutation[suc_id].append(mean(uf_mutation_li[suc_id][instance_id]))
                median_mutation[suc_id].append(median(uf_mutation_li[suc_id][instance_id]))
            else:
                average_mutation[suc_id].append(0)
                median_mutation[suc_id].append(0)

            if uf_goal_li[suc_id][instance_id]:
                average_goal[suc_id].append(mean(uf_goal_li[suc_id][instance_id]))
                median_goal[suc_id].append(median(uf_goal_li[suc_id][instance_id]))
            else:
                average_goal[suc_id].append(0)
                median_goal[suc_id].append(0)

    return (average_mutation, average_goal), (median_mutation, median_goal)


def draw_bar_charts(inst_per_subp, uf_num, average_mutation, average_goal, median_mutation, median_goal):

    width=0.35

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

        for id in range(inst_per_subp):
            instance_id=instance_subp_id+id

            print("The times for instance {} that achieved global optima is {}, times that didn't achieved is {}"
                .format(instance_id, uf_num[0][instance_id], uf_num[1][instance_id]))

            if uf_num[0][instance_id]!=0:
                print("The average mutation to achieve global optima {} is {}".
                    format(average_goal[0][instance_id], average_mutation[0][instance_id]))

            if uf_num[1][instance_id]!=0:
                print("The average maximum goal achieved within {} steps is {}".
                    format(average_mutation[1][instance_id], average_goal[1][instance_id]))

        ax_lst[int(instance_subp_id/inst_per_subp), 1].\
            bar(x_ind, np.array(average_goal[1][instance_subp_id:instance_subp_id+inst_per_subp]), width, label="")
        ax_lst[int(instance_subp_id/inst_per_subp), 2].\
            bar(x_ind, np.array(average_mutation[0][instance_subp_id:instance_subp_id+inst_per_subp]), width, label="")

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

def dump_to_file(filename, **kwargs):
    with open(filename, 'a') as f:
        for k, v in kwargs.items():
            f.write(k+'\n')
            f.write(json.dumps(v)+'\n')

def loads_from_file(filename, *argv):
    res=[None]*len(argv)
    with open(filename, 'r') as f:
        while True:
            line=f.readline()
            if not line:
                break
            if line[:-1].lower() in argv:
                res[argv.index(line[:-1].lower())]=json.loads(f.readline())

    return tuple(res)

if __name__ == '__main__':
    main()

