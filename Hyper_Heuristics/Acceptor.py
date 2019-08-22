import abc, logging
from random import choice, choices
from multiprocessing import Pool


class Acceptor(abc.ABC):
    def __init__(self, benchmark):
        self._benchmark=benchmark

    @abc.abstractmethod
    def accept(self):
        pass

    @property
    def benchmark(self):
        return self._benchmark

    @benchmark.setter
    def benchmark(self, benchmark):
        self._benchmark=benchmark

    @staticmethod
    def acceptor_factory(class_name, *args):
        for cls in Acceptor.all_subclasses(Acceptor):
            if cls.__name__.lower()==class_name.lower():
                return cls(*args)

        return None

    @staticmethod
    def all_subclasses(cls):
        return set(cls.__subclasses__()). \
            union([s for c in cls.__subclasses__() for s in Acceptor.all_subclasses(c)])


class AM(Acceptor):
    def accept(self):
        mutate_fun=choice(self.benchmark.mutates())
        goal_b=self.benchmark.goal(self.benchmark.current_solution)
        mutations, mutated_bits, goal_a=self.benchmark.mutate(mutate_fun[0], *mutate_fun[1])
        self.benchmark.apply(mutations)
        logging.debug("chosen mutation operator: {} IS ACCEPTED by acceptor: {} "
                      "with mutations {} on {}, goal_a: {}".
                      format(mutate_fun[0], "AM",
                             mutations, mutated_bits, goal_a))

        return True, 1, goal_a

    def __str__(self):
        return "AM"

class OI(Acceptor):
    def accept(self):
        mutate_fun=choice(self.benchmark.mutates())
        goal_b=self.benchmark.goal(self.benchmark.current_solution)
        mutations, mutated_bits, goal_a=self.benchmark.mutate(mutate_fun[0], *mutate_fun[1])
        if goal_a>goal_b:
            self.benchmark.apply(mutations)
            logging.debug("chosen mutation operator: {} IS ACCEPTED by acceptor: {} "
                          "with mutations {} on {}, goal_a: {}".
                          format(mutate_fun[0], "OI",
                                 mutations, mutated_bits, goal_a))
            return True, 1, goal_a

        logging.debug("chosen mutation operator: {} IS NOT ACCEPTED by acceptor: {} "
                      "with mutations {} on {}, goal_a: {}".
                      format(mutate_fun[0], "OI",
                             mutations, mutated_bits, goal_a))
        return False, 1, goal_a

    def __str__(self):
        return "OI"

class IE(Acceptor):
    def accept(self):
        mutate_fun=choice(self.benchmark.mutates())
        goal_b=self.benchmark.goal(self.benchmark.current_solution)
        mutations, mutated_bits, goal_a=self.benchmark.mutate(mutate_fun[0], *mutate_fun[1])
        if goal_a>=goal_b:
            self.benchmark.apply(mutations)
            logging.debug("chosen mutation operator: {} IS ACCEPTED by acceptor: {} "
                          "with mutations {} on {}, goal_a: {}".
                          format(mutate_fun.__name__, "IE",
                                 mutations, mutated_bits, goal_a))
            return True, 1, goal_a

        logging.debug("chosen mutation operator: {} IS NOT ACCEPTED by acceptor: {} "
                      "with mutations {} on {}, goal_a: {}".
                      format(mutate_fun.__name__, "IE",
                             mutations, mutated_bits, goal_a))
        return False, 1, goal_a

    def __str__(self):
        return "IE"

#==============================================================================
# Command line processing
class Greedy(Acceptor):
    def __init__(self, benchmark):
        super().__init__(benchmark)
        self.num_mutation=len(benchmark.mutates())
        self.pool=Pool(processes=self.num_mutation)

    def accept(self):
        goal_b=self.benchmark.goal(self.benchmark.current_solution)
        mutate_para=self.benchmark.mutates()
        # multi_result=[self.pool.apply_async(self.benchmark.mutate, (mutate_para[i][0], *mutate_para[i][1], ))
        #               for i in range(self.num_mutation)]
        multi_result=list()
        for i in range(self.num_mutation):
            multi_result.append(self.pool.apply_async(self.benchmark.mutate, (mutate_para[i][0], *mutate_para[i][1])))

        acceptable_index=list()
        # acceptable_mutation=list()
        # acceptable_goal_a=list()
        # self.pool.close()
        # self.pool.join()

        for i in len(multi_result):
            mutations, mutated_bits, goal_a=multi_result[i].get(timeout=1)
            if goal_a>=goal_b:
                acceptable_index.append(i)
                # acceptable_goal_a.append(goal_a)
                # acceptable_mutation.append(mutations)
                logging.debug("chosen mutation operator: {} COULD be ACCEPTED by acceptor: {} " 
                              "with mutations {} on {}, goal_a: {}".
                              format(self.benchmark.mutates()[i][0], "Greedy",
                                     mutations, mutated_bits, goal_a))
            else:
                logging.debug("chosen mutation operator: {} CANNOT be ACCEPTED by acceptor: {} "
                              "with mutations {} on {}, goal_a: {}".
                              format(self.benchmark.mutates()[i][0], "Greedy",
                                     mutations, mutated_bits, goal_a))

        if acceptable_index:
            selected_index=choice(acceptable_index)
            selected_result=multi_result[selected_index].get()
            self.benchmark.apply(selected_result[0])

            logging.debug("chosen mutation operator: {} is ACCEPTED by acceptor: {} "
                          "with mutations {} on {}, goal_a: {}".
                          format(self.benchmark.mutates()[selected_index][0], "Greedy",
                                 selected_result[0], selected_result[1], selected_result[2]))
            return True, len(multi_result), selected_result[2]
        else:
            logging.debug("No mutation operator is NOT ACCEPTED by acceptor: {} ".format("Greedy"))
            return False, len(multi_result), goal_b

    def __str__(self):
        return "Greedy"

class GeneralisedGreedy(Greedy):

    def __init__(self, benchmark, generalised_mutates=5):
        super().__init__(benchmark)
        self.tau=generalised_mutates

    def accept(self):
        goal_b=self.benchmark.goal(self.benchmark.current_solution)
        mutate_para=self.benchmark.mutates()
        # multi_result=[self.pool.apply_async(self.benchmark.mutate, (mutate_para[i][0], *mutate_para[i][1]))
        #               for i in range(self.num_mutation)]
        multi_result=list()
        for i in range(self.num_mutation):
            multi_result.append(self.pool.apply_async(self.benchmark.mutate, (mutate_para[i][0], *mutate_para[i][1])))

        acceptable_index=list()
        # acceptable_mutation=list()
        # acceptable_goal_a=list()
        # self.pool.close()
        # self.pool.join()

        for i in range(len(multi_result)):
            mutations, mutated_bits, goal_a=multi_result[i].get(timeout=1)
            if goal_a>=goal_b:
                acceptable_index.append(i)
                # acceptable_goal_a.append(goal_a)
                # acceptable_mutation.append(mutations)
                logging.info("GeneralisedGreedy could accept mutation{}, goal_b: {}, goal_a: {}".
                              format(mutations, goal_b, goal_a))
            else:
                logging.info("GeneralisedGreedy cannot accept mutation{}, goal_b: {}, goal_a: {}".
                              format(mutations, goal_b, goal_a))

        if acceptable_index:
            selected_index=choice(acceptable_index)
            selected_result=multi_result[selected_index].get()
            goal_a=selected_result[2]
            self.benchmark.apply(selected_result[0])

            logging.info("chosen mutation operator: {} is ACCEPTED by acceptor: {} "
                          "with mutations {} on {}, goal_a: {}".
                          format(self.benchmark.mutates()[selected_index][0], "GeneralisedGreedy",
                                 selected_result[0], selected_result[1], goal_a))

            for _ in range(self.tau-1):
                mutations, mutated_bits, goal_a=self.benchmark.mutate(mutate_para[selected_index][0], *mutate_para[selected_index][1])
                self.benchmark.apply(mutations)

                logging.info("chosen mutation operator: {} is ACCEPTED by acceptor: {} "
                              "with mutations {} on {}, goal_a: {}".
                              format(self.benchmark.mutates()[selected_index][0], "GeneralisedGreedy",
                                     mutations, mutated_bits, goal_a))


            return True, len(multi_result)+self.tau-1, goal_a
        else:
            logging.info("chosen acceptor: {} IS NOT accepted: {} with mutation {} on {}, goal_b: {}, goal_a: {}".
                          format(None, "GeneralisedGreedy", None, None, goal_b, None))
            return False, len(multi_result), goal_b


    def __str__(self):
        return "GeneralisedGreedy"

class GeneralisedRandomGradient(Acceptor):

    def accept(self):
        pass

    def __str__(self):
        return "GeneralisedRandomGradient"

