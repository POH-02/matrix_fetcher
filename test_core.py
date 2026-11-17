import asyncio
import pytest
import httpx
from unittest.mock import AsyncMock, patch, MagicMock

from matrix_fetcher import get_matrix, NetworkError, ServerError, ParseError

SOURCE_URL = 'https://raw.githubusercontent.com/avito-tech/python-trainee-assignment/main/matrix.txt'
TRAVERSAL = [
    10, 50, 90, 130,
    140, 150, 160, 120,
    80, 40, 30, 20,
    60, 100, 110, 70,
]


@pytest.mark.asyncio
async def test_get_matrix_real():
    """Интеграционный тест с реальным сетевым запросом."""
    result = await get_matrix(SOURCE_URL)
    assert result == TRAVERSAL


@pytest.mark.asyncio
async def test_get_matrix_network_error():
    """Проверка обработки сетевых ошибок (например, Connection Refused)."""
    with patch('matrix_fetcher.core.httpx.AsyncClient') as mock_client_class:
        mock_client = AsyncMock()
        mock_client.get.side_effect = httpx.RequestError("Connection refused", request=MagicMock())
        mock_client_class.return_value.__aenter__.return_value = mock_client
        
        with pytest.raises(NetworkError) as exc_info:
            await get_matrix("http://invalid.local")
        
        assert "Connection refused" in str(exc_info.value)


@pytest.mark.asyncio
async def test_get_matrix_server_error():
    """Проверка обработки ошибок сервера (5xx)."""
    with patch('matrix_fetcher.core.httpx.AsyncClient') as mock_client_class:
        mock_client = AsyncMock()
        mock_response = AsyncMock()
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "500 Internal Server Error", 
            request=MagicMock(), 
            response=MagicMock(status_code=500)
        )
        mock_client.get.return_value = mock_response
        mock_client_class.return_value.__aenter__.return_value = mock_client
        
        with pytest.raises(ServerError) as exc_info:
            await get_matrix("http://example.com/error")
        
        assert "500" in str(exc_info.value)


@pytest.mark.asyncio
async def test_get_matrix_parse_error():
    """Проверка обработки некорректных данных (не квадратная матрица)."""
    with patch('matrix_fetcher.core.httpx.AsyncClient') as mock_client_class:
        mock_client = AsyncMock()
        mock_response = AsyncMock()
        mock_response.text = "+---+\n| 1 |\n+---+\n| 2 | 3 |\n+---+---+"
        mock_response.raise_for_status = AsyncMock()
        mock_client.get.return_value = mock_response
        mock_client_class.return_value.__aenter__.return_value = mock_client
        
        with pytest.raises(ParseError) as exc_info:
            await get_matrix("http://example.com/bad-matrix")
        
        assert "не является квадратной" in str(exc_info.value)
