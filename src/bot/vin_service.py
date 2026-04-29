from __future__ import annotations

from typing import Any

import httpx

NHTSA_URL = "https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVin/{vin}?format=json"
VINDECODER_URL = "https://api.vindecoder.eu/3.2"


class VinService:
    def __init__(self, timeout: float = 10.0) -> None:
        self.timeout = timeout

    async def decode(self, vin: str) -> dict[str, Any]:
        data = await self._decode_nhtsa(vin)
        if data.get("Make") and data.get("Model"):
            return {"source": "nhtsa", **data}
        return {"source": "nhtsa", **data}

    async def _decode_nhtsa(self, vin: str) -> dict[str, Any]:
        url = NHTSA_URL.format(vin=vin)
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(url)
            response.raise_for_status()
        payload = response.json()
        results = payload.get("Results", [])
        fields = {x.get("Variable"): x.get("Value") for x in results if x.get("Variable")}
        return {
            "VIN": vin,
            "Make": fields.get("Make"),
            "Model": fields.get("Model"),
            "ModelYear": fields.get("Model Year"),
            "BodyClass": fields.get("Body Class"),
            "Engine": fields.get("Engine Configuration") or fields.get("Engine Model"),
            "FuelType": fields.get("Fuel Type - Primary"),
            "DriveType": fields.get("Drive Type"),
            "PlantCountry": fields.get("Plant Country"),
        }
