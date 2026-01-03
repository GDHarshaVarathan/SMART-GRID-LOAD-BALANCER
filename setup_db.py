import sqlite3

# This line CREATES smart_grid.db if it does not exist
conn = sqlite3.connect("smart_grid.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS machines (
    machine_id INTEGER PRIMARY KEY,
    name TEXT,
    priority TEXT,
    max_power_kw REAL
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS sensor_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    machine_id INTEGER,
    timestamp DATETIME,
    power_kw REAL,
    state TEXT,
    FOREIGN KEY(machine_id) REFERENCES machines(machine_id)
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS tariff (
    hour INTEGER,
    rate_per_kwh REAL
)
""")

conn.commit()
conn.close()

print("Database smart_grid.db created successfully.")
