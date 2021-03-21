from enum import Enum
from core.exceptions import ValidationParamError, NotFoundParamError


class TaskType(Enum):
    MIN = 'MIN'
    MAX = 'MAX'


class Data(object):
    def __init__(self, params):
        self._validate_params(params)

        self.type = self.read_type(params['type'])
        self.c = params['c']
        self.restrictions = params['restrictions']
        self.comparisonOperators = params['comparisonOperators']
        self.b = params['b']

    @staticmethod
    def read_type(_type):
        if _type == TaskType.MAX.value:
            return TaskType.MAX
        if _type == TaskType.MIN.value:
            return TaskType.MIN

        raise ValidationParamError('The parameter: {} = {} has an unexpected value'.format('type', _type))

    def _validate_params(self, params):
        self._validate_ex_param(params)
        self._validate_len_param(params)
        self._validate_comparison_operators(params['comparisonOperators'])

    @staticmethod
    def _validate_ex_param(params):
        if 'type' not in params:
            raise NotFoundParamError('type')
        if 'c' not in params:
            raise NotFoundParamError('c')
        if 'restrictions' not in params:
            raise NotFoundParamError('restrictions')
        if 'comparisonOperators' not in params:
            raise NotFoundParamError('comparisonOperators')
        if 'b' not in params:
            raise NotFoundParamError('b')

    @staticmethod
    def _validate_len_param(params):
        if (len(params['restrictions']) != len(params['comparisonOperators'])
                or len(params['comparisonOperators']) != len(params['b'])):
            raise ValidationParamError('Dimensions of matrices are not valid: restrictions={}, comparisonOperators={}, '
                                       'b={}'.format(len(params['restrictions']),
                                                     len(params['comparisonOperators']),
                                                     len(params['b'])))
        for index in range(len(params['restrictions'])):
            if len(params['c']) != len(params['restrictions'][index]):
                raise ValidationParamError('Dimensions of matrices are not valid: c={}, restrictions[{}]={}'.format(
                    len(params['c']),
                    index,
                    len(params['restrictions'][0])))

    @staticmethod
    def _validate_comparison_operators(params):
        for index in range(len(params)):
            if params[index] not in ['<=', '>=', '=']:
                raise ValidationParamError('Unknown comparison operator: {}'.format(params[index]))
