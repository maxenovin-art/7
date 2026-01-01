
from fastapi import FastAPI, HTTPException
import sqlite3
from datetime import datetime

app = FastAPI()
DB_NAME = "/tmp/database.db"

def get_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price REAL,
            stock INTEGER
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            quantity INTEGER,
            date TEXT
        )
    """)

    conn.commit()
    return conn

@app.get("/")
def root():
    return {"status": "Inventory API is running"}

@app.post("/products")
def add_product(name: str, price: float, stock: int):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO products (name, price, stock) VALUES (?, ?, ?)",
        (name, price, stock)
    )
    conn.commit()
    conn.close()
    return {"message": "Product added"}

@app.post("/sales")
def add_sale(product_id: int, quantity: int):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT stock FROM products WHERE id=?", (product_id,))
    row = cur.fetchone()

    if not row or row[0] < quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")

    cur.execute(
        "UPDATE products SET stock = stock - ? WHERE id=?",
        (quantity, product_id)
    )

    cur.execute(
        "INSERT INTO sales (product_id, quantity, date) VALUES (?, ?, ?)",
        (product_id, quantity, datetime.now().isoformat())
    )

    conn.commit()
    conn.close()
    return {"message": "Sale recorded"}
