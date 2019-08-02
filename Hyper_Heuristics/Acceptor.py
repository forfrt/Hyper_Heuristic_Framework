import abc


class Acceptor(abc.ABC):


    @abc.abstractmethod
    def accept(self, goal_before, goal_after):
        pass


class AM(Acceptor):
    def accept(self, goal_before, goal_after):
        mutation, goal_b, goal_a=self.benchmark.mutate()
        self.benchmark.apply()

        return True

    def __str__(self):
        return "AM"

class OI(Acceptor):
    def accept(self, goal_before, goal_after):
        return True if goal_after>goal_before else False

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
