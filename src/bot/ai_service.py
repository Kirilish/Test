from __future__ import annotations

import httpx


class AIService:
    def __init__(self, api_token: str, model: str, timeout: float = 30.0) -> None:
        self.api_token = api_token
        self.model = model
        self.timeout = timeout

    async def ask(self, question: str, car_context: dict | None, plan: str = "free") -> str:
        if not self.api_token:
            return self._fallback_answer(question, car_context, plan)

        prompt = self._build_prompt(question, car_context, plan)
        url = f"https://api-inference.huggingface.co/models/{self.model}"
        headers = {"Authorization": f"Bearer {self.api_token}"}

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.post(url, headers=headers, json={"inputs": prompt, "options": {"wait_for_model": True}})
            resp.raise_for_status()
        payload = resp.json()
        if isinstance(payload, list) and payload:
            return payload[0].get("generated_text", "Не удалось получить ответ от ИИ.")[:4000]
        return "Не удалось получить ответ от ИИ."

    def _build_prompt(self, question: str, car_context: dict | None, plan: str) -> str:
        car_text = "Нет данных об автомобиле."
        if car_context:
            car_text = ", ".join(f"{k}: {v}" for k, v in car_context.items() if v)
        plan_hint = "PRO: подробные шаги диагностики и варианты запчастей" if plan == "pro_99_stars" else "FREE: краткие рекомендации"
        return (
            "Ты автоассистент. Отвечай по-русски, структурировано. "
            "Если есть риск — советуй обратиться на СТО.\n"
            f"Тариф: {plan_hint}\n"
            f"Автомобиль: {car_text}\n"
            f"Вопрос: {question}\nОтвет:"
        )

    def _fallback_answer(self, question: str, car_context: dict | None, plan: str) -> str:
        detail = (
            "1) Проверьте уровни жидкостей. 2) Считайте OBD-II коды. 3) Проверьте утечки и АКБ."
            if plan == "pro_99_stars"
            else "Проверьте регламент ТО и базовые OBD-II ошибки."
        )
        car_hint = ""
        if car_context and car_context.get("Make") and car_context.get("Model"):
            car_hint = f" ({car_context['Make']} {car_context['Model']})"
        return f"Вопрос{car_hint}: {question}\nРекомендация: {detail}"
