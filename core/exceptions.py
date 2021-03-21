class BusinessLogicException(BaseException):
    def __init__(self, message):
        super().__init__(message)


class ValidationParamError(BusinessLogicException):
    def __init__(self, message):
        super().__init__(message)


class NotFoundParamError(BusinessLogicException):
    def __init__(self, param_name):
        message = 'Not found parameter by key: {}'.format(param_name)
        super().__init__(message)
