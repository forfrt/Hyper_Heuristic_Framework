
import abc


class Base(abc.ABC):

    @property
    @abc.abstractmethod
    def _current_solution(self):
        return 'Should never reach here'

    @_current_solution.setter
    @abc.abstractmethod
    def _current_solution(self, new__current_solution):
        return


class PartialImplementation(Base):

    @property
    def _current_solution(self):
        return 'Read-only'


class Implementation(Base):

    _current_solution = 'Default _current_solution'

    def __init__(self, _current_solution):
        self._current_solution=_current_solution

    @property
    def current_solution(self):
        return self._current_solution

    @current_solution.setter
    def current_solution(self, new__current_solution):
        self._current_solution = new__current_solution


try:
    b = Base()
    print('Base._current_solution:', b._current_solution)
except Exception as err:
    print('ERROR:', str(err))

p = PartialImplementation()
print('PartialImplementation._current_solution:', p._current_solution)

try:
    p._current_solution = 'Alteration'
    print('PartialImplementation._current_solution:', p._current_solution)
except Exception as err:
    print('ERROR:', str(err))

i = Implementation("hello")
print('Implementation._current_solution:', i._current_solution)

i._current_solution = 'world'
print('Changed _current_solution:', i._current_solution)