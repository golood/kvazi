class ValidationParamError(Exception):
    def __init__(self, message):
        super().__init__(message)


class NotFoundParamError(Exception):
    def __init__(self, param_name):
        message = 'Not found parameter by key: {}'.format(param_name)
        super().__init__(message)
