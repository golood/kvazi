from core.dto import Data, TaskType
from pulp import LpVariable, LpProblem, LpAffineExpression, LpStatus, value
from pulp.constants import LpMinimize, LpMaximize


class LpSolve(object):
    def __init__(self):
        self.vars = None
        self.problem = None
        self.result = None

    def get_var(self, index: int):
        return self.vars.get('x{}'.format(index))

    def run(self):
        status = self.problem.solve()
        return self.is_status_optimal(LpStatus[status])

    def get_result(self) -> dict:
        x = {'c': None, 'var': {}}

        variables = self.problem.variables()
        for index in range(len(variables)):
            x['var'].setdefault(variables[index].name, variables[index].varValue)

        x['c'] = value(self.problem.objective)
        return x

    @staticmethod
    def is_status_optimal(status):
        if status == "Optimal":
            return True
        return False


class Builder(object):

    def build_lp(self, data: Data) -> LpSolve:
        lp_solve = LpSolve()

        self.build_vars(lp_solve, data)
        self.build_problems(lp_solve, data)
        self.build_problem_c(lp_solve, data)
        self.build_problem_restrictions(lp_solve, data)

        return lp_solve

    def build_vars(self, lp_solve: LpSolve, data: Data):
        pass

    @staticmethod
    def build_problems(lp_solve: LpSolve, data: Data):
        pass

    @staticmethod
    def build_problem_c(lp_solve: LpSolve, data: Data):
        pass

    def build_problem_restrictions(self, lp_solve: LpSolve, data: Data):
        pass


class BuilderLp(Builder):

    def build_vars(self, lp_solve: LpSolve, data: Data):
        _vars = dict()
        for index in range(1, len(data.c) + 1):
            var_name = 'x{}'.format(index)
            _vars.setdefault(var_name, LpVariable(var_name, lowBound=0))

        lp_solve.vars = _vars

    @staticmethod
    def build_problems(lp_solve: LpSolve, data: Data):
        if data.type == TaskType.MIN:
            lp_solve.problem = LpProblem('Задача_ЛП', LpMinimize)
            return
        if data.type == TaskType.MAX:
            lp_solve.problem = LpProblem('Задача_ЛП', LpMaximize)
            return
        raise TypeError

    @staticmethod
    def build_problem_c(lp_solve: LpSolve, data: Data):
        _params = []

        for index in range(1, len(lp_solve.vars) + 1):
            _params.append((lp_solve.get_var(index), data.c[index - 1],))

        lp_solve.problem += LpAffineExpression(_params, name='Целевая_функция')

    def build_problem_restrictions(self, lp_solve: LpSolve, data: Data):
        for index_restriction in range(len(data.comparisonOperators)):
            _params = []
            for index in range(1, len(lp_solve.vars) + 1):
                _params.append((lp_solve.get_var(index), data.restrictions[index_restriction][index - 1],))

            self.create_restriction(
                lp_solve,
                _params,
                data.comparisonOperators[index_restriction],
                data.b[index_restriction],
                index_restriction)

    @staticmethod
    def create_restriction(lp_solve: LpSolve, _params, operator, b, index):
        if operator == '<=':
            lp_solve.problem += LpAffineExpression(_params) <= b, str(index)
        if operator == '>=':
            lp_solve.problem += LpAffineExpression(_params) >= b, str(index)
        if operator == '=':
            lp_solve.problem += LpAffineExpression(_params) == b, str(index)


class BuilderLpKvazi(Builder):

    def build_vars(self, lp_solve: LpSolve, data: Data):
        _vars = dict()

        for index in range(1, self._get_count_var(data) + 1):
            var_name = 'x{}'.format(index)
            _vars.setdefault(var_name, LpVariable(var_name, lowBound=0))

        lp_solve.vars = _vars

    @staticmethod
    def build_problems(lp_solve: LpSolve, data: Data):
        pass

    @staticmethod
    def build_problem_c(lp_solve: LpSolve, data: Data):
        pass

    def build_problem_restrictions(self, lp_solve: LpSolve, data: Data):
        pass

    @staticmethod
    def _get_count_var(data: Data) -> int:
        count = len(data.c)

        for item in data.comparisonOperators:
            if item == '=':
                count += 2
            else:
                count += 1

        return count


class ModelData(object):
    def __init__(self):
        self.dataDTO = None
        self.solve = None
        self.solveKvazi = None

    def solve_task(self):
        builder = BuilderLp()
        self.solve = builder.build_lp(self.dataDTO)

        success = self.solve.run()

        if not success:
            print("Решение не найдено, идёт поиск квазирешения.")
            self.solve = None
            builder = BuilderLpKvazi()
            self.solveKvazi = builder.build_lp(self.dataDTO)

            return

        print("Решение успешно найдено.")

    def get_result(self):
        if self.solve is not None:
            return self.solve.get_result()
        if self.solveKvazi is not None:
            return self.solveKvazi.get_result()

        return None
