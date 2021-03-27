class BusinessLogicException(BaseException):
    """
    Базовое исключение, возникает при нарушении бизнес логики.
    """

    def __init__(self, message):
        super().__init__(message)


class ValidationParamError(BusinessLogicException):
    """
    Исключение возникает, при наличии не валидных параметров.
    """

    def __init__(self, message):
        super().__init__(message)


class NotFoundParamError(BusinessLogicException):
    """
    Исключение возникает, когда не удалось найти ожидаемый параметр.
    """

    def __init__(self, param_name):
        message = 'Not found parameter by key: {}'.format(param_name)
        super().__init__(message)
