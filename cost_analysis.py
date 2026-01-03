import sqlite3
import pandas as pd

conn = sqlite3.connect("smart_grid.db")

query = """
SELECT 
    sd.timestamp,
    m.max_power_kw AS power_kw,
    t.rate_per_kwh
FROM sensor_data sd
JOIN machines m ON sd.machine_id = m.machine_id
JOIN tariff t
ON CAST(strftime('%H', sd.timestamp) AS INTEGER) = t.hour
"""

df_base = pd.read_sql(query, conn)
conn.close()

df_base['timestamp'] = pd.to_datetime(df_base['timestamp'], format='ISO8601')

INTERVAL_HOURS = 5 / 3600
df_base['cost'] = df_base['power_kw'] * df_base['rate_per_kwh'] * INTERVAL_HOURS

baseline_cost = df_base['cost'].sum()
print("Baseline cost (₹):", round(baseline_cost, 2))

conn = sqlite3.connect("smart_grid.db")

query = """
SELECT 
    sd.timestamp,
    sd.power_kw,
    sd.state,
    t.rate_per_kwh
FROM sensor_data sd
JOIN tariff t
ON CAST(strftime('%H', sd.timestamp) AS INTEGER) = t.hour
"""

df_opt = pd.read_sql(query, conn)
conn.close()

df_opt['timestamp'] = pd.to_datetime(df_opt['timestamp'], format='ISO8601')

df_opt.loc[df_opt['state'] == 'OFF', 'power_kw'] = 0

df_opt['cost'] = df_opt['power_kw'] * df_opt['rate_per_kwh'] * INTERVAL_HOURS

optimized_cost = df_opt['cost'].sum()
print("Optimized cost (₹):", round(optimized_cost, 2))

savings_pct = ((baseline_cost - optimized_cost) / baseline_cost) * 100
print("Cost savings:", round(savings_pct, 2), "%")
