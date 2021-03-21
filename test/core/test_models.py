import unittest
from core.models import LpSolve, Builder
from core.dto import TaskType, Data
from pulp.constants import LpMaximize, LpMinimize
from pulp import LpVariable


def get_expect_data_max():
    params = {
        "type": "MAX",
        "c": [1, 2, -3, 2],
        "restrictions": [
            [1, 2, 4, 5],
            [0, 4, -4, 0]
        ],
        "comparisonOperators": ["<=", "="],
        "b": [2, 3]
    }
    return Data(params)


def get_expect_data_min():
    params = {
        "type": "MIN",
        "c": [1, 2, -3, 2],
        "restrictions": [
            [1, 2, 4, 5],
            [0, 4, -4, 0]
        ],
        "comparisonOperators": ["<=", "="],
        "b": [2, 3]
    }
    return Data(params)


class TestBuilder(unittest.TestCase):
    def test_build_vars(self):
        count_var = 4
        actual = Builder()
        actual.build_vars(get_expect_data_min())
        self.assertEqual(count_var, len(actual.lpSolve.vars))
        self.assertEqual(actual.lpSolve.vars['x1'].name, 'x1')

    def test_build_problems(self):
        actual = Builder()
        actual.build_problems(get_expect_data_min())
        self.assertEqual(actual.lpSolve.problem.sense, LpMinimize)
        actual.build_problems(get_expect_data_max())
        self.assertEqual(actual.lpSolve.problem.sense, LpMaximize)
        self.assertRaises(TypeError, Builder.build_problems, None)
        self.assertRaises(TypeError, Builder.build_problems, 1)

    def test_get_var(self):
        actual = Builder()
        actual.build_vars(get_expect_data_min())
        expect = LpVariable('x1', lowBound=0)
        self.assertEqual(actual.lpSolve.get_var(1).toDict(), expect.toDict())
        expect = LpVariable('x2', lowBound=0)
        self.assertEqual(actual.lpSolve.get_var(2).toDict(), expect.toDict())
        self.assertEqual(actual.lpSolve.get_var(5), None)

    def test_build_problem_c(self):
        actual = Builder()
        actual.build_vars(get_expect_data_min())
        actual.build_problems(get_expect_data_min())
        actual.build_problem_c((get_expect_data_min()))
        self.assertEqual(actual.lpSolve.problem.objective.name, 'Целевая_функция')
        self.assertEqual(actual.lpSolve.problem.objective.toDict(),
              [{'name': 'x1', 'value': 1},
               {'name': 'x2', 'value': 2},
               {'name': 'x3', 'value': -3},
               {'name': 'x4', 'value': 2}])

    def test_build_problem_restrictions(self):
        actual = Builder()
        actual.build_vars(get_expect_data_min())
        actual.build_problems(get_expect_data_min())
        actual.build_problem_c(get_expect_data_min())
        actual.build_problem_restrictions(get_expect_data_min())
        self.assertEqual(str(actual.lpSolve.problem.constraints.get('0')), 'x1 + 2*x2 + 4*x3 + 5*x4 <= 2')
        self.assertEqual(str(actual.lpSolve.problem.constraints.get('1')), '0*x1 + 4*x2 - 4*x3 + 0*x4 = 3')


if __name__ == '__main__':
    unittest.main()
