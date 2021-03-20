import unittest
from core.models import LpSolve
from core.dto import TaskType
from pulp.constants import LpMaximize, LpMinimize


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


if __name__ == '__main__':
    unittest.main()
