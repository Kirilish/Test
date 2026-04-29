from bot.storage import JsonStorage


def test_free_and_pro_limits(tmp_path):
    store = JsonStorage(str(tmp_path / "users.json"))
    ok1, _ = store.add_car(1, {"VIN": "1"})
    ok2, _ = store.add_car(1, {"VIN": "2"})
    assert ok1 is True
    assert ok2 is False

    store.upgrade_to_pro(1)
    ok3, _ = store.add_car(1, {"VIN": "2"})
    assert ok3 is True
