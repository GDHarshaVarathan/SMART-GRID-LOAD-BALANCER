import sqlite3

conn = sqlite3.connect("smart_grid.db")
cur = conn.cursor()

cur.execute("DELETE FROM tariff")

for hour in range(24):
    rate = 9 if 18 <= hour <= 22 else 6
    cur.execute("INSERT INTO tariff VALUES (?, ?)", (hour, rate))

conn.commit()
conn.close()

print("Tariff table populated.")
