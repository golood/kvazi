from core.dto import Data, TaskType
from pulp import LpVariable, LpProblem, LpAffineExpression
from pulp.constants import LpMinimize, LpMaximize


class LpSolve(object):
    def __init__(self, data: Data):
        self.c = data.c
        self.x = None
        self.vars = self._build_vars(len(data.c))
        self.problem = self._build_problems(data.type)

        self._build_problem_c()

    @staticmethod
    def _build_vars(count_var: int) -> dict:
        _vars = dict()
        for index in range(1, count_var + 1):
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

    def _build_problem_c(self):
        _params = []

        for index in range(1, len(self.vars) + 1):
            _params.append((self.get_var(index), self.c[index - 1],))

        self.problem += LpAffineExpression(_params, name='Целевая_функция')

    def get_var(self, index: int):
        return self.vars.get('x{}'.format(index))

    def run(self):
        self.problem.solve()

    def get_result(self) -> dict:
        pass
