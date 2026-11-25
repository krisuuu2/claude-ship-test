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
    _, total, due = shop.place_order(db, cid, [(30.0, 1)], date(2026, 11, 25))
    assert total == 45.0
    assert due == date(2026, 12, 25)


def test_no_code_means_no_discount():
    assert shop.order_total([(100.0, 3)]) == 300.0


def test_find_customers_by_name():
    db = shop.connect(":memory:")
    shop.add_customer(db, "Anna Nowak", "anna@example.com")
    assert len(shop.find_customers(db, "Anna")) == 1
