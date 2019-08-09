import logging, glob

from Hyper_Heuristics.HH import *
from Hyper_Heuristics.Satlib import *
from Hyper_Heuristics.Acceptor import *
from Hyper_Heuristics.LeadingOne import *

def test_leadingone():
    am=AM()
    oi=OI()

    oneMax=OneMax(probability=0.2, n=100)
    hh_one=HH([am, oi], [0, 1], oneMax)
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
    am=AM()
    oi=OI()

    logging.basicConfig(filename="hh.log", level=logging.INFO,
                        format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

    # test_leadingone()

    max_step=200000
    num_instance=20
    hh_sat=HH([am, oi], [0.02, 1], None, max_step) # 2/n
    opt_sat('./satlib/uf50/*.cnf', num_instance, hh_sat)


def opt_sat(file_pattern, num, hh_sat):

    uf20_li=glob.glob(file_pattern)
    uf20_num=[0]*2
    uf20_step=[0]*2
    uf20_goal=[0]*2

    for uf20 in uf20_li[:num]:
        sat=Sat(uf20)
        sat.print_inner_var()
        hh_sat.set_benchmark(sat)
        hh_sat.optimize()
        hh_sat.stat()

        # find global optima within max_step
        if hh_sat.max_goal==sat.num_cla:
            uf20_num[0]+=1
            uf20_goal[0]+=sat.num_cla
            uf20_step[0]+=hh_sat.num_step
        # didn't find global optima within max_step
        else:
            uf20_num[1]+=1
            uf20_goal[1]+=hh_sat.max_goal
            uf20_step[1]+=hh_sat.max_step

        logging.info("------------")

    print("num of instances that achieved global optima is {}, instances that didn't achieved is {}"
          .format(uf20_num[0], uf20_num[1]))

    if uf20_num[0]!=0:
        print("The average step to achieve global optima {} is {}".format(uf20_goal[0]/uf20_num[0], uf20_step[0]/uf20_num[0]))

    if uf20_num[1]!=0:
        print("The average maximum goal achieved within {} steps is {}".format(uf20_step[1]/uf20_num[1], uf20_goal[1]/uf20_num[1]))

main()

