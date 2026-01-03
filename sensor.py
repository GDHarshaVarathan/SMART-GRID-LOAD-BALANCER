import sqlite3
import random
from datetime import datetime
import time

conn = sqlite3.connect("smart_grid.db")
cur = conn.cursor()

machines = [
    (1, "CNC Machine", "HIGH", 6.0),
    (2, "Air Compressor", "MEDIUM", 4.0),
    (3, "Conveyor Belt", "LOW", 3.0)
]

cur.executemany("INSERT OR IGNORE INTO machines VALUES (?, ?, ?, ?)", machines)
conn.commit()

def generate_power(max_kw):
    return round(random.uniform(0.6, 1.0) * max_kw, 2)

while True:
    for m in machines:
        power = generate_power(m[3])
        cur.execute("""
        INSERT INTO sensor_data (machine_id, timestamp, power_kw, state)
        VALUES (?, ?, ?, ?)
        """, (m[0], datetime.now().isoformat(), power, "ON"))

    conn.commit()
    time.sleep(5)
