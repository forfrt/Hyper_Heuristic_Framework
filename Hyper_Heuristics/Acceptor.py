import abc, logging


class Acceptor(abc.ABC):

    @abc.abstractmethod
    def accept(self, benchmark):
        pass


class AM(Acceptor):
    def accept(self, benchmark):
        mutation, mutated_bit, goal_b, goal_a=benchmark.mutate()
        benchmark.apply()
        logging.debug("choosen acceptor: {} is accepted: {} with mutation {} on {}, goal_b: {}, goal_a: {}".
                      format("AM", True, mutation, mutated_bit, goal_b, goal_a))

        return True, 1, goal_a

    def __str__(self):
        return "AM"

class OI(Acceptor):
    def accept(self, benchmark):
        mutation, mutated_bit, goal_b, goal_a=benchmark.mutate()
        if goal_a>goal_b:
            benchmark.apply()
            logging.debug("choosen acceptor: {} is accepted: {} with mutation {} on {}, goal_b: {}, goal_a: {}".
                          format("OI", True, mutation, mutated_bit, goal_b, goal_a))
            return True, 1, goal_a

        logging.debug("choosen acceptor: {} is accepted: {} with mutation {} on {}, goal_b: {}, goal_a: {}".
                      format("OI", False, mutation, mutated_bit, goal_b, goal_a))
        return False, 1, goal_a

    def __str__(self):
        return "OI"

class IE(Acceptor):
    def accept(self, goal_before, goal_after):
        return True if goal_after>=goal_before else False

    def __str__(self):
        return "IE"

class GeneralisedGreedy(Acceptor):
    def accept(self, goal_before, goal_after):
        return True if goal_after>=goal_before else False

    def __str__(self):
        return "IE"

class GeneralisedGreedy(Acceptor):
    def accept(self, goal_before, goal_after):
        return True if goal_after>=goal_before else False

    def __str__(self):
        return "IE"
