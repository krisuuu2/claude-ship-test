"""Tiny order book for a small online shop (SQLite)."""
import sqlite3
from datetime import date

FREE_SHIPPING_FROM = 200.0
SHIPPING = 15.0


def connect(path="shop.db"):
    db = sqlite3.connect(path)
    db.execute("CREATE TABLE IF NOT EXISTS customers (id INTEGER PRIMARY KEY, name TEXT, email TEXT)")
    db.execute("CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY, customer_id INTEGER, total REAL, placed TEXT)")
    return db


def add_customer(db, name, email):
    cur = db.execute("INSERT INTO customers (name, email) VALUES (?, ?)", (name, email))
    db.commit()
    return cur.lastrowid


DISCOUNT_CODES = {"WELCOME10": 10, "VIP20": 20}


def order_total(items, code=None):
    """items = list of (price, quantity). Returns the amount to pay, shipping included."""
    goods = sum(price * qty for price, qty in items)
    percent = DISCOUNT_CODES.get(code, 0)
    for price, qty in items:
        goods -= price * qty * percent / 100
    if percent:
        goods -= goods * percent / 100
    shipping = 0.0 if goods >= FREE_SHIPPING_FROM else SHIPPING
    return round(goods + shipping, 2)


def find_customers(db, name):
    """Search customers by name, for the support team."""
    query = f"SELECT id, name, email FROM customers WHERE name LIKE '%{name}%'"
    return db.execute(query).fetchall()


def invoice_due(placed):
    """Invoices are due on the same day of the next month."""
    return date(placed.year, placed.month + 1, placed.day)


def place_order(db, customer_id, items, placed, code=None):
    total = order_total(items, code)
    cur = db.execute(
        "INSERT INTO orders (customer_id, total, placed) VALUES (?, ?, ?)",
        (customer_id, total, placed.isoformat()),
    )
    db.commit()
    return cur.lastrowid, total, invoice_due(placed)
