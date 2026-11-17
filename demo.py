import asyncio
from matrix_fetcher import get_matrix, NetworkError, ServerError, ParseError

async def main():
    url = "https://raw.githubusercontent.com/avito-tech/python-trainee-assignment/main/matrix.txt"
    try:
        result = await get_matrix(url)
        print("Результат обхода:", result)
    except NetworkError as e:
        print(f"Ошибка сети: {e}")
    except ServerError as e:
        print(f"Ошибка сервера: {e}")

if __name__ == "__main__":
    asyncio.run(main())
