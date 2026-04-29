from __future__ import annotations

import json
from collections import Counter
from datetime import date, datetime
from pathlib import Path
from typing import Any

FREE_CAR_LIMIT = 1
PRO_CAR_LIMIT = 3
FREE_AI_LIMIT = 20
PRO_AI_LIMIT = 200


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

    def _ensure_user(self, user_id: int) -> None:
        data = self._read()
        key = str(user_id)
        if key not in data:
            data[key] = {
                "plan": "free",
                "cars": [],
                "active_car": 0,
                "ai_used": 0,
                "history": [],
                "questions": [],
                "upgraded_at": None,
                "last_seen": datetime.utcnow().isoformat(),
            }
            self._write(data)

    def get_profile(self, user_id: int) -> dict[str, Any]:
        self._ensure_user(user_id)
        data = self._read()
        data[str(user_id)]["last_seen"] = datetime.utcnow().isoformat()
        self._write(data)
        return data[str(user_id)]

    def get_ai_limit(self, plan: str) -> int:
        return PRO_AI_LIMIT if plan == "pro_99_stars" else FREE_AI_LIMIT

    def can_use_ai(self, user_id: int) -> tuple[bool, str]:
        profile = self.get_profile(user_id)
        limit = self.get_ai_limit(profile["plan"])
        if profile["ai_used"] >= limit:
            return False, f"Достигнут лимит ИИ ({limit}/мес). Перейдите на PRO: /upgrade_99"
        return True, "ok"

    def mark_ai_usage(self, user_id: int, question: str) -> None:
        data = self._read()
        self._ensure_user(user_id)
        data = self._read()
        rec = data[str(user_id)]
        rec["ai_used"] += 1
        rec["questions"].append({"q": question, "ts": datetime.utcnow().isoformat()})
        self._write(data)

    def upgrade_to_pro(self, user_id: int) -> None:
        data = self._read()
        self._ensure_user(user_id)
        data = self._read()
        data[str(user_id)]["plan"] = "pro_99_stars"
        data[str(user_id)]["upgraded_at"] = datetime.utcnow().isoformat()
        self._write(data)

    def add_car(self, user_id: int, car: dict[str, Any]) -> tuple[bool, str]:
        data = self._read()
        self._ensure_user(user_id)
        data = self._read()
        rec = data[str(user_id)]
        limit = PRO_CAR_LIMIT if rec["plan"] == "pro_99_stars" else FREE_CAR_LIMIT
        if len(rec["cars"]) >= limit:
            return False, f"Лимит машин для тарифа: {limit}"
        car.setdefault("nickname", f"{car.get('Make', 'Car')} {car.get('Model', '')}".strip())
        car.setdefault("mileage", 0)
        rec["cars"].append(car)
        rec["active_car"] = len(rec["cars"]) - 1
        self._write(data)
        return True, "ok"

    def list_cars(self, user_id: int) -> list[dict[str, Any]]:
        return self.get_profile(user_id).get("cars", [])

    def get_active_car(self, user_id: int) -> dict[str, Any] | None:
        profile = self.get_profile(user_id)
        cars = profile.get("cars", [])
        if not cars:
            return None
        idx = min(profile.get("active_car", 0), len(cars) - 1)
        return cars[idx]

    def set_active_car(self, user_id: int, index: int) -> bool:
        data = self._read()
        self._ensure_user(user_id)
        data = self._read()
        rec = data[str(user_id)]
        if index < 0 or index >= len(rec["cars"]):
            return False
        rec["active_car"] = index
        self._write(data)
        return True

    def add_service_record(self, user_id: int, title: str, mileage: int, cost: float, category: str) -> None:
        data = self._read()
        self._ensure_user(user_id)
        data = self._read()
        rec = data[str(user_id)]
        rec["history"].append({
            "title": title,
            "mileage": mileage,
            "cost": cost,
            "category": category,
            "date": date.today().isoformat(),
            "car": self.get_active_car(user_id),
        })
        car = self.get_active_car(user_id)
        if car:
            car["mileage"] = max(car.get("mileage", 0), mileage)
        self._write(data)

    def service_history(self, user_id: int) -> list[dict[str, Any]]:
        return self.get_profile(user_id).get("history", [])

    def expense_stats(self, user_id: int) -> dict[str, Any]:
        history = self.service_history(user_id)
        total = round(sum(float(x.get("cost", 0)) for x in history), 2)
        by_cat: dict[str, float] = {}
        for item in history:
            cat = item.get("category", "other")
            by_cat[cat] = round(by_cat.get(cat, 0) + float(item.get("cost", 0)), 2)
        return {"total": total, "by_category": by_cat, "count": len(history)}

    def analytics(self) -> dict[str, Any]:
        data = self._read()
        users = len(data)
        pro_users = sum(1 for x in data.values() if x.get("plan") == "pro_99_stars")
        cars = [f"{c.get('Make')} {c.get('Model')}".strip() for u in data.values() for c in u.get("cars", [])]
        questions = [q.get("q", "") for u in data.values() for q in u.get("questions", [])]
        return {
            "users": users,
            "pro_users": pro_users,
            "revenue_stars": pro_users * 99,
            "popular_cars": Counter(cars).most_common(5),
            "popular_questions": Counter(questions).most_common(5),
        }
