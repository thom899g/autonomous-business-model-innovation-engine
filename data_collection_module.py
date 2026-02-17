import asyncio
from typing import Dict, List
import aiohttp
from tenacity import retry, stop_after_attempt

class DataCollector:
    def __init__(self):
        self.session = None

    async def fetch_data(self, url: str) -> Dict:
        """Fetches data from a given URL asynchronously."""
        try:
            if not self.session:
                self.session = aiohttp.ClientSession()
            async with self.session.get(url) as response:
                if response.status == 200:
                    return await response.json()
                raise ValueError(f"API returned {response.status}")
        except Exception as e:
            raise

    @retry(stop=stop_after_attempt(3))
    async def async_fetch(self, sources: List[str]) -> Dict:
        """Fetches data from multiple sources with retry logic."""
        tasks = [self.fetch_data(source) for source in sources]
        results = await asyncio.gather(*tasks)
        return {source: result for source, result in zip(sources, results)}