import sys, pathlib
from datetime import date

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import shop


def test_shipping_added_below_threshold():
    assert shop.order_total([(50.0, 2)]) == 115.0


def test_free_shipping_from_threshold():
    assert shop.order_total([(100.0, 2)]) == 200.0


def test_place_order_saves_total():
    db = shop.connect(":memory:")
    cid = shop.add_customer(db, "Anna", "anna@example.com")
    _, total = shop.place_order(db, cid, [(30.0, 1)], date(2026, 11, 25))
    assert total == 45.0
