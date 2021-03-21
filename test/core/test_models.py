import unittest
from core.models import LpSolve
from core.dto import TaskType, Data
from pulp.constants import LpMaximize, LpMinimize
from pulp import LpVariable


def get_expect_data():
    params = {
        "type": "MIN",
        "c": [1, 2, -3, 2],
        "restrictions": [
            [1, 2, 4, 5],
            [0, 4, -4, 0]
        ],
        "comparisonOperators": ["<", "="],
        "b": [2, 3]
    }
    return Data(params)


class TestBuildLpSolve(unittest.TestCase):
    def test_build_vars(self):
        count_var = 2
        actual = LpSolve._build_vars(count_var)
        self.assertEqual(count_var, len(actual))
        self.assertEqual(actual['x1'].name, 'x1')

    def test_build_problems(self):
        actual = LpSolve._build_problems(TaskType.MAX)
        self.assertEqual(actual.sense, LpMaximize)
        actual = LpSolve._build_problems(TaskType.MIN)
        self.assertEqual(actual.sense, LpMinimize)
        self.assertRaises(TypeError, LpSolve._build_problems, None)
        self.assertRaises(TypeError, LpSolve._build_problems, 1)

    def test_get_var(self):
        actual = LpSolve(get_expect_data())
        expect = LpVariable('x1', lowBound=0)
        self.assertEqual(actual.get_var(1).toDict(), expect.toDict())
        expect = LpVariable('x2', lowBound=0)
        self.assertEqual(actual.get_var(2).toDict(), expect.toDict())
        self.assertEqual(actual.get_var(5), None)

    def test_build_problem_c(self):
        actual = LpSolve(get_expect_data())
        self.assertEqual(actual.problem.objective.name, 'Целевая_функция')
        self.assertEqual(actual.problem.objective.toDict(),
              [{'name': 'x1', 'value': 1},
               {'name': 'x2', 'value': 2},
               {'name': 'x3', 'value': -3},
               {'name': 'x4', 'value': 2}])


if __name__ == '__main__':
    unittest.main()
