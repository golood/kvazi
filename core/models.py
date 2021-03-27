from abc import ABC, abstractmethod
from core.dto import Data, TaskType
from pulp import LpVariable, LpProblem, LpAffineExpression, LpStatus, value
from pulp.constants import LpMinimize, LpMaximize


class LpSolve(object):
    """
    Задача линейного программирования.
    """

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
    def is_status_optimal(status) -> bool:
        """
        Проверяет статус решения задачи ЛП.
        :return: True - в случае успешного решения задачи.
                 False - в случае, когда не удалось решить задачу ЛП.
        """

        if status == "Optimal":
            return True
        return False


class Builder(ABC):
    """
    Строитель задачи ЛП.
    """

    def build_lp(self, data: Data) -> LpSolve:
        """
        Шаблонный метод для создания задачи ЛП.
        """

        lp_solve = LpSolve()

        self.build_vars(lp_solve, data)
        self.build_problems(lp_solve, data)
        self.build_problem_c(lp_solve, data)
        self.build_problem_restrictions(lp_solve, data)

        return lp_solve

    @staticmethod
    @abstractmethod
    def build_vars(lp_solve: LpSolve, data: Data):
        """
        Создаёт переменные для задачи ЛП.
        """
        pass

    @staticmethod
    @abstractmethod
    def build_problems(lp_solve: LpSolve, data: Data):
        """
        Создаёт задачу ЛП на поиск минимума или максимума.
        """
        pass

    @staticmethod
    @abstractmethod
    def build_problem_c(lp_solve: LpSolve, data: Data):
        """
        Создаёт целевую функцию задачи ЛП.
        """
        pass

    @staticmethod
    @abstractmethod
    def build_problem_restrictions(lp_solve: LpSolve, data: Data):
        """
        Создаёт ограничения для задачи ЛП.
        """
        pass

    @staticmethod
    def create_restriction(lp_solve: LpSolve, _params: list, operator: str, b, index):
        """
        Вспомогательная функция для создания ограничения.
        :param lp_solve: задача ЛП.
        :param _params: массив параметров ограничения.
        :param operator: оператор сравнения ограничения.
        :param b: числовое значение правой части ограничения.
        :param index: порядковый номер ограничений.
        """

        if operator == '<=':
            lp_solve.problem += LpAffineExpression(_params) <= b, str(index)
        if operator == '>=':
            lp_solve.problem += LpAffineExpression(_params) >= b, str(index)
        if operator == '=':
            lp_solve.problem += LpAffineExpression(_params) == b, str(index)


class BuilderLp(Builder):
    """
    Строитель задачи ЛП.
    """

    @staticmethod
    def build_vars(lp_solve: LpSolve, data: Data):
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

    @staticmethod
    def build_problem_restrictions(lp_solve: LpSolve, data: Data):
        for index_restriction in range(len(data.comparisonOperators)):
            _params = []
            for index in range(1, len(lp_solve.vars) + 1):
                _params.append((lp_solve.get_var(index), data.restrictions[index_restriction][index - 1],))

            Builder.create_restriction(
                lp_solve,
                _params,
                data.comparisonOperators[index_restriction],
                data.b[index_restriction],
                index_restriction)


class BuilderLpKvazi(Builder):
    """
    Строитель задачи ЛП для поиска квазирешения.
    """

    @staticmethod
    def build_vars(lp_solve: LpSolve, data: Data):
        _vars = dict()

        for index in range(1, BuilderLpKvazi._get_count_var(data) + 1):
            var_name = 'x{}'.format(index)
            _vars.setdefault(var_name, LpVariable(var_name, lowBound=0))

        lp_solve.vars = _vars

    @staticmethod
    def build_problems(lp_solve: LpSolve, data: Data):
        lp_solve.problem = LpProblem('Задача_ЛП', LpMinimize)

    @staticmethod
    def build_problem_c(lp_solve: LpSolve, data: Data):
        _params = []

        for index in range(len(data.c) + 1, BuilderLpKvazi._get_count_var(data) + 1):
            _params.append((lp_solve.get_var(index), 1,))

        lp_solve.problem += LpAffineExpression(_params, name='Целевая_функция')

    @staticmethod
    def build_problem_restrictions(lp_solve: LpSolve, data: Data):
        index_kvazi_var = len(data.c) + 1

        for index_restriction in range(len(data.comparisonOperators)):
            _params = []
            for index in range(1, len(data.c) + 1):
                _params.append((lp_solve.get_var(index), data.restrictions[index_restriction][index - 1],))

            if data.comparisonOperators[index_restriction] == '>=':
                _params.append((lp_solve.get_var(index_kvazi_var), 1,))
                index_kvazi_var += 1
            if data.comparisonOperators[index_restriction] == '<=':
                _params.append((lp_solve.get_var(index_kvazi_var), -1,))
                index_kvazi_var += 1
            if data.comparisonOperators[index_restriction] == '=':
                _params.append((lp_solve.get_var(index_kvazi_var), 1,))
                index_kvazi_var += 1
                _params.append((lp_solve.get_var(index_kvazi_var), -1,))
                index_kvazi_var += 1

            Builder.create_restriction(
                lp_solve,
                _params,
                data.comparisonOperators[index_restriction],
                data.b[index_restriction],
                index_restriction)

    @staticmethod
    def _get_count_var(data: Data) -> int:
        """
        Получает количество переменных для задачи ЛП.
        """

        count = len(data.c)

        for item in data.comparisonOperators:
            if item == '=':
                count += 2
            else:
                count += 1

        return count


class ModelData(object):
    """
    Модель данных.
    """

    def __init__(self):
        self.dataDTO = None
        self.solve = None
        self.solveKvazi = None

    def solve_task(self) -> bool:
        """
        Решение задачи ЛП.
        :return True - в случае, если удалось найти решение или квазирешение задачи ЛП.
                False - в случае, если не удалось найти решение и квазирешение задачи ЛП.
        """

        builder = BuilderLp()
        self.solve = builder.build_lp(self.dataDTO)

        success = self.solve.run()

        if not success:
            print("Решение не найдено, идёт поиск квазирешения.")
            self.solve = None
            builder = BuilderLpKvazi()
            self.solveKvazi = builder.build_lp(self.dataDTO)
            success = self.solveKvazi.run()

            if success:
                print("Квазирешение успешно найдено.")
                return True

            print("Не удалось найти квазирешение.")
            return False

        print("Решение успешно найдено.")
        return True

    def get_result(self):
        """
        Получает результаты решения задачи ЛП.
        """

        if self.solve is not None:
            return self.solve.get_result()
        if self.solveKvazi is not None:
            return self.solveKvazi.get_result()

        return None
