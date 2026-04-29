from __future__ import annotations

import json
from pathlib import Path
from typing import Any

FREE_CAR_LIMIT = 1
PRO_CAR_LIMIT = 2


class JsonStorage:
    def __init__(self, path: str = "data/users.json") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("{}", encoding="utf-8")

    def _read(self) -> dict[str, Any]:
        return json.loads(self.path.read_text(encoding="utf-8"))

    def _write(self, data: dict[str, Any]) -> None:
        self.path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def _ensure_user(self, user_id: int) -> dict[str, Any]:
        data = self._read()
        key = str(user_id)
        if key not in data:
            data[key] = {"plan": "free", "cars": [], "active_car": 0}
            self._write(data)
        return data[key]

    def get_profile(self, user_id: int) -> dict[str, Any]:
        self._ensure_user(user_id)
        return self._read()[str(user_id)]

    def upgrade_to_pro(self, user_id: int) -> None:
        data = self._read()
        self._ensure_user(user_id)
        data = self._read()
        data[str(user_id)]["plan"] = "pro_99_stars"
        self._write(data)

    def add_car(self, user_id: int, car: dict[str, Any]) -> tuple[bool, str]:
        data = self._read()
        key = str(user_id)
        if key not in data:
            data[key] = {"plan": "free", "cars": [], "active_car": 0}

        plan = data[key]["plan"]
        limit = PRO_CAR_LIMIT if plan == "pro_99_stars" else FREE_CAR_LIMIT
        if len(data[key]["cars"]) >= limit:
            return False, f"Лимит машин для тарифа: {limit}"

        data[key]["cars"].append(car)
        data[key]["active_car"] = len(data[key]["cars"]) - 1
        self._write(data)
        return True, "ok"

    def get_active_car(self, user_id: int) -> dict[str, Any] | None:
        profile = self.get_profile(user_id)
        cars = profile.get("cars", [])
        if not cars:
            return None
        idx = profile.get("active_car", 0)
        if idx >= len(cars):
            idx = 0
        return cars[idx]

    def list_cars(self, user_id: int) -> list[dict[str, Any]]:
        return self.get_profile(user_id).get("cars", [])

    def set_active_car(self, user_id: int, index: int) -> bool:
        data = self._read()
        key = str(user_id)
        if key not in data or index < 0 or index >= len(data[key].get("cars", [])):
            return False
        data[key]["active_car"] = index
        self._write(data)
        return True
