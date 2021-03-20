from dto import Data
from pulp import LpVariable


class LpSolve(object):
    def __init__(self, data: Data):
        self.c = None
        self.x = None
        self.vars = self._build_vars(len(data.c))
        self.problem = None

    @staticmethod
    def _build_vars(count_var: int) -> dict:
        _vars = dict()
        for index in range(count_var):
            var_name = 'x{}'.format(index)
            _vars.setdefault(var_name, LpVariable(var_name, lowBound=0))

        return _vars

    def run(self):
        self.problem.solve()

    def get_result(self) -> dict:
        pass
