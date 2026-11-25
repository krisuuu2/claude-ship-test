"""Tiny order book for a small online shop (SQLite)."""
import sqlite3

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


def order_total(items):
    """items = list of (price, quantity). Returns the amount to pay, shipping included."""
    goods = sum(price * qty for price, qty in items)
    shipping = 0.0 if goods >= FREE_SHIPPING_FROM else SHIPPING
    return round(goods + shipping, 2)


def place_order(db, customer_id, items, placed):
    total = order_total(items)
    cur = db.execute(
        "INSERT INTO orders (customer_id, total, placed) VALUES (?, ?, ?)",
        (customer_id, total, placed.isoformat()),
    )
    db.commit()
    return cur.lastrowid, total
