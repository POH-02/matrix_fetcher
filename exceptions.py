class MatrixFetcherError(Exception):
    """Базовое исключение для библиотеки matrix_fetcher."""
    pass


class NetworkError(MatrixFetcherError):
    """Вызывается при сетевых ошибках (таймаут, отказ в соединении и т.д.)."""
    pass


class ServerError(MatrixFetcherError):
    """Вызывается при ошибках на стороне сервера (HTTP статусы 4xx, 5xx)."""
    pass


class ParseError(MatrixFetcherError):
    """Вызывается, если содержимое ответа не может быть разобрано как корректная матрица."""
    pass
