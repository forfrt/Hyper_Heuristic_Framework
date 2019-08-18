import argparse

cli=argparse.ArgumentParser()
cli.add_argument("-b", "--benchmark",
                 help="BENCHMARK : the benchmark to be tested on (Benchmark in {OneMax, Cliff, Jump, Sat default: Sat}")
cli.add_argument("-s", "--show", action="store_true", help="show the statistic bar chart based on pervious data")
cli.add_argument("--sat_files", default="./", help="CNF files if SAT benchmark is selected")
cli.add_argument("--acceptors", nargs="+", default=["am", "oi"], help="a list of acceptors chosen to be selected")
cli.add_argument("--acceptor_probs", nargs="+", type=float, default=[1, 1], help="probabilities of given acceptors")
cli.add_argument("--max_mutation", type=int, default="200000", help="maximum number of mutation")
cli.add_argument("--num_instance", type=int, default=100, help="number of instance to be tested")
cli.add_argument("--num_run", type=int, default=100, help="number of run for each problem instance")
cli.add_argument("--log_file", default="hh.log", help="logging file")
cli.add_argument("--dump_file", default="sat.log", help="file that store the json.dumps() result")

args=cli.parse_args()

print(args, type(args))
