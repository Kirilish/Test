from bot.storage import JsonStorage


def test_limits_and_ai_usage(tmp_path):
    s = JsonStorage(str(tmp_path / "u.json"))
    assert s.add_car(1, {"VIN": "A"})[0] is True
    assert s.add_car(1, {"VIN": "B"})[0] is False

    s.upgrade_to_pro(1)
    assert s.add_car(1, {"VIN": "B"})[0] is True
    assert s.add_car(1, {"VIN": "C"})[0] is True

    ok, _ = s.can_use_ai(1)
    assert ok is True
    for _ in range(201):
        s.mark_ai_usage(1, "q")
    ok, _ = s.can_use_ai(1)
    assert ok is False
