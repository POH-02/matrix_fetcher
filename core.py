import httpx
from typing import List

from .exceptions import NetworkError, ServerError, ParseError


async def get_matrix(url: str) -> List[int]:
    """
    Получает квадратную матрицу по указанному URL и возвращает список целых чисел
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
    except httpx.HTTPStatusError as e:
        raise ServerError(f"HTTP ошибка при запросе матрицы: {e}") from e
    except httpx.RequestError as e:
        raise NetworkError(f"Сетевая ошибка при запросе матрицы: {e}") from e

    text = response.text.strip()
    if not text:
        raise ParseError("Получен пустой ответ от сервера")

    matrix = _parse_matrix(text)
    if not matrix:
        raise ParseError("Не удалось извлечь данные матрицы из ответа")
    
    # Дополнительная валидация: проверка на квадратность
    n = len(matrix)
    for row in matrix:
        if len(row) != n:
            raise ParseError("Матрица не является квадратной (NxN)")

    return _traverse_spiral_ccw(matrix)


def _parse_matrix(text: str) -> List[List[int]]:
    """Парсит ASCII-представление матрицы в список списков целых чисел."""
    matrix = []
    for line in text.split('\n'):
        line = line.strip()
        # Пропускаем пустые строки и строки границ, состоящие из '+' и '-'
        if not line or line.startswith('+'):
            continue
        
        if line.startswith('|'):
            # Разделяем по '|' и отфильтровываем пустые части по краям
            parts = [part.strip() for part in line.split('|') if part.strip()]
            try:
                row = [int(part) for part in parts]
            except ValueError as e:
                raise ParseError(f"Не удалось преобразовать элемент в число в строке: {line}") from e
            matrix.append(row)
            
    return matrix


def _traverse_spiral_ccw(matrix: List[List[int]]) -> List[int]:
    """
    Осуществляет обход квадратной матрицы по спирали против часовой стрелки,
    начиная с левого верхнего угла.
    """
    if not matrix or not matrix[0]:
        return []
    
    result = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1
    
    while top <= bottom and left <= right:
        # 1. Обход вниз по левому столбцу
        for i in range(top, bottom + 1):
            result.append(matrix[i][left])
        left += 1
        
        # 2. Обход вправо по нижней строке
        for i in range(left, right + 1):
            result.append(matrix[bottom][i])
        bottom -= 1
        
        if top <= bottom and left <= right:
            # 3. Обход вверх по правому столбцу
            for i in range(bottom, top - 1, -1):
                result.append(matrix[i][right])
            right -= 1
            
            # 4. Обход влево по верхней строке
            for i in range(right, left - 1, -1):
                result.append(matrix[top][i])
            top += 1
            
    return result
