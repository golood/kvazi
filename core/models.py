from core.dto import Data, TaskType
from pulp import LpVariable, LpProblem, LpAffineExpression
from pulp.constants import LpMinimize, LpMaximize


class LpSolve(object):
    def __init__(self):
        self.vars = None
        self.problem = None
        self.result = None

    def get_var(self, index: int):
        return self.vars.get('x{}'.format(index))

    def run(self):
        self.problem.solve()

    def get_result(self) -> dict:
        pass


class Builder(object):
    def __init__(self):
        self.lpSolve = LpSolve()

    def build_lp_solve(self, data: Data) -> LpSolve:
        self.build_vars(data)
        self.build_problems(data)
        self.build_problem_c(data)
        self.build_problem_restrictions(data)

        return self.lpSolve

    def build_vars(self, data: Data):
        _vars = dict()
        for index in range(1, len(data.c) + 1):
            var_name = 'x{}'.format(index)
            _vars.setdefault(var_name, LpVariable(var_name, lowBound=0))

        self.lpSolve.vars = _vars

    def build_problems(self, data: Data):
        if data.type == TaskType.MIN:
            self.lpSolve.problem = LpProblem('Задача_ЛП', LpMinimize)
            return
        if data.type == TaskType.MAX:
            self.lpSolve.problem = LpProblem('Задача_ЛП', LpMaximize)
            return
        raise TypeError

    def build_problem_c(self, data: Data):
        _params = []

        for index in range(1, len(self.lpSolve.vars) + 1):
            _params.append((self.lpSolve.get_var(index), data.c[index - 1],))

        self.lpSolve.problem += LpAffineExpression(_params, name='Целевая_функция')

    def build_problem_restrictions(self, data: Data):
        for index_restriction in range(len(data.comparisonOperators)):
            _params = []
            for index in range(1, len(self.lpSolve.vars) + 1):
                _params.append((self.lpSolve.get_var(index), data.restrictions[index_restriction][index - 1],))

            self.create_restriction(
                _params,
                data.comparisonOperators[index_restriction],
                data.b[index_restriction],
                index_restriction)

    def create_restriction(self, _params, operator, b, index):
        if operator == '<=':
            self.lpSolve.problem += LpAffineExpression(_params) <= b, str(index)
        if operator == '>=':
            self.lpSolve.problem += LpAffineExpression(_params) >= b, str(index)
        if operator == '=':
            self.lpSolve.problem += LpAffineExpression(_params) == b, str(index)


class ModelData(object):
    def __init__(self):
        self.dataDTO = None
        self.solve = None
        self.solveKvazi = None
