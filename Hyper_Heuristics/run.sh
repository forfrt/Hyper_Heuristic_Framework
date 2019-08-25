#!/bin/bash

#! test
python main.py -b sat --sat_files ./satlib/uf75 --num_instance 5 --num_run 5 --acceptor_probs 0.0133 0.9866 --max_mutation 100000000 --log_file ./log/uf75_test.log --dump_file ./log/uf75_test.dump > ./log/uf75_test.print
python main.py -b sat --sat_files ./satlib/uf50 --num_instance 5 --num_run 5 --acceptor_probs 0.02 0.98 --max_mutation 1000000 --log_file ./log/uf50_test.log --dump_file ./log/uf50_test.dump > ./log/uf50_test.print
python main.py -b sat --sat_files ./satlib/uf20 --num_instance 5 --num_run 5 --acceptor_probs 0.05 0.95 --max_mutation 10000 --log_file ./log/uf20_test.log --dump_file ./log/uf50_test.dump > ./log/uf50_test.print

python main.py -b sat --sat_files ./satlib/uf75 --num_instance 100 --num_run 100 --acceptor_probs 0.0133 0.9866 --max_mutation 100000000 --log_file ./log/uf75_0.0133.log --dump_file ./log/uf75_0.0133.dump > ./log/uf75_0.0133.print
python main.py -b sat --sat_files ./satlib/uf75 --num_instance 100 --num_run 100 --acceptor_probs 0.0266 0.9733 --max_mutation 100000000 --log_file ./log/uf75_0.0266.log --dump_file ./log/uf75_0.0266.dump > ./log/uf75_0.0266.print
python main.py -b sat --sat_files ./satlib/uf75 --num_instance 100 --num_run 100 --acceptor_probs 0 1.0 --max_mutation 100000000 --log_file ./log/uf75_0.log --dump_file ./log/uf75_0.dump > ./log/uf75_0.print
python main.py -b sat --sat_files ./satlib/uf75 --num_instance 100 --num_run 100 --acceptor_probs 1.0 0 --max_mutation 100000000 --log_file ./log/uf75_1.log --dump_file ./log/uf75_1.dump > ./log/uf75_1.print

python main.py -b sat --sat_files ./satlib/uf50 --num_instance 100 --num_run 100 --acceptor_probs 0.02 0.98 --max_mutation 1000000 --log_file ./log/uf50_0.02.log --dump_file ./log/uf50_0.02.dump > ./log/uf50_0.02.print
python main.py -b sat --sat_files ./satlib/uf50 --num_instance 100 --num_run 100 --acceptor_probs 0.04 0.96 --max_mutation 1000000 --log_file ./log/uf50_0.04.log --dump_file ./log/uf50_0.04.dump > ./log/uf50_0.04.print
python main.py -b sat --sat_files ./satlib/uf50 --num_instance 100 --num_run 100 --acceptor_probs 0 1.0 --max_mutation 100000000 --log_file ./log/uf50_0.log --dump_file ./log/uf50_0.dump > ./log/uf50_0.print
python main.py -b sat --sat_files ./satlib/uf50 --num_instance 100 --num_run 100 --acceptor_probs 1.0 0 --max_mutation 100000000 --log_file ./log/uf50_1.log --dump_file ./log/uf50_1.dump > ./log/uf50_1.print

python main.py -b sat --sat_files ./satlib/uf20 --num_instance 100 --num_run 100 --acceptor_probs 0.05 0.95 --max_mutation 10000 --log_file ./log/uf20.05.log --dump_file ./log/uf50_0.05.dump > ./log/uf50_0.05.print
python main.py -b sat --sat_files ./satlib/uf20 --num_instance 100 --num_run 100 --acceptor_probs 0.1 0.9 --max_mutation 10000 --log_file ./log/uf20_0.1.log --dump_file ./log/uf50_0.1.dump > ./log/uf50_0.1.print
python main.py -b sat --sat_files ./satlib/uf20 --num_instance 100 --num_run 100 --acceptor_probs 0 1.0 --max_mutation 100000000 --log_file ./log/uf20_0.log --dump_file ./log/uf20_0.dump > ./log/uf20_0.print
python main.py -b sat --sat_files ./satlib/uf20 --num_instance 100 --num_run 100 --acceptor_probs 1.0 0 --max_mutation 100000000 --log_file ./log/uf20_1.log --dump_file ./log/uf20_1.dump > ./log/uf20_1.print

#$ -l rmem=2G
#$ -l rmem=2G
