from bot.main import _format_car


def test_format_car_contains_fields():
    text = _format_car({"VIN": "X", "Make": "BMW", "Model": "X5", "ModelYear": "2020"})
    assert "BMW" in text
    assert "X5" in text
