import aiohttp

from src.config import settings


async def validate_spy_cat_breed(breed: str) -> bool:
    url = settings.CAT_BREED_API_URL
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                raise Exception(f"Failed to fetch data from API. Status: {response.status}")

            data = await response.json()

            if breed in tuple(cat.get("id") for cat in data):
                return True
            return False