from core.dto import Data, TaskType
from pulp import LpVariable, LpProblem
from pulp.constants import LpMinimize, LpMaximize


class LpSolve(object):
    def __init__(self, data: Data):
        self.c = None
        self.x = None
        self.vars = self._build_vars(len(data.c))
        self.problem = self._build_problems(data.type)

    @staticmethod
    def _build_vars(count_var: int) -> dict:
        _vars = dict()
        for index in range(count_var):
            var_name = 'x{}'.format(index)
            _vars.setdefault(var_name, LpVariable(var_name, lowBound=0))

        return _vars

    @staticmethod
    def _build_problems(_type: TaskType) -> LpProblem:
        if _type == TaskType.MIN:
            return LpProblem('Задача_ЛП', LpMinimize)
        if _type == TaskType.MAX:
            return LpProblem('Задача_ЛП', LpMaximize)
        raise TypeError

    def run(self):
        self.problem.solve()

    def get_result(self) -> dict:
        pass
