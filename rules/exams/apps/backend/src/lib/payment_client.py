import httpx
from typing import Dict, Any

class ExternalAPIClient:
    """외부 타사 결제 API 등 외부 엔드포인트 연동을 담당하는 HTTP 클라이언트 어댑터"""
    def __init__(self, base_url: str, timeout: float = 5.0):
        self.base_url = base_url
        self.timeout = timeout

    async def fetch_data(self, endpoint: str) -> Dict[str, Any]:
        async with httpx.AsyncClient(base_url=self.base_url, timeout=self.timeout) as client:
            response = await client.get(endpoint)
            response.raise_for_status()
            return response.json()
