import unittest
from core.dto import Data, TaskType
from core.exceptions import ValidationParamError, NotFoundParamError


class TestData(unittest.TestCase):
    def test_validate_ex_param(self):
        self.assertRaises(NotFoundParamError, Data._validate_ex_param, {'typee': ''})
        self.assertRaises(NotFoundParamError, Data._validate_ex_param, {'type': '', 'cv': []})
        self.assertRaises(NotFoundParamError, Data._validate_ex_param, {'type': '', 'c': [], 'restrictionss': []})
        self.assertRaises(NotFoundParamError, Data._validate_ex_param, {'type': '', 'c': [], 'restrictions': [],
                                                                        'comparisonOperatorss': []})
        self.assertRaises(NotFoundParamError, Data._validate_ex_param, {'type': '', 'c': [], 'restrictions': [],
                                                                        'comparisonOperators': [], 'bv': []})
        self.assertIsNone(Data._validate_ex_param({'type': '', 'c': [], 'restrictions': [],
                                                   'comparisonOperators': [], 'b': []}))

    def test_validate_len_param(self):
        obj = {'type': '', 'c': [1, 1], 'restrictions': [[2, 4], [1, 1]],
               'comparisonOperators': ['<', '>'], 'b': [4, 5]}
        self.assertIsNone(Data._validate_len_param(obj))
        obj['b'] = [3]
        self.assertRaises(ValidationParamError, Data._validate_len_param, obj)

        obj['b'] = [4, 4]
        obj['restrictions'] = [[2, 4], [1, 1, 5]]
        self.assertRaises(ValidationParamError, Data._validate_len_param, obj)

    def test_validate_comparison_operators(self):
        self.assertIsNone(Data._validate_comparison_operators(['<=', '>=', '=']))
        self.assertRaises(ValidationParamError, Data._validate_comparison_operators, ['=<', '<', '>'])

    def test_read_type(self):
        actual = Data.read_type('MIN')
        self.assertEqual(TaskType.MIN, actual)

        actual = Data.read_type('MAX')
        self.assertEqual(TaskType.MAX, actual)

        self.assertRaises(ValidationParamError, Data.read_type, 'MAXv')
        self.assertRaises(ValidationParamError, Data.read_type, None)


if __name__ == '__main__':
    unittest.main()
