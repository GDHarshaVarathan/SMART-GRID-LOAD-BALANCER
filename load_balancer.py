import sqlite3

GRID_LIMIT_KW = 12.0

def apply_load_balancing(predicted_load):
    conn = sqlite3.connect("smart_grid.db")
    cur = conn.cursor()

    if predicted_load <= GRID_LIMIT_KW:
        print("Load within limit. No action required.")
        conn.close()
        return

    print(f"Predicted load {predicted_load:.2f} kW exceeds limit.")

    # Step 1: Shut down LOW priority machines
    cur.execute("""
        UPDATE sensor_data
        SET state='OFF'
        WHERE machine_id IN (
            SELECT machine_id FROM machines WHERE priority='LOW'
        )
    """)
    conn.commit()

    print("LOW priority machines turned OFF.")

    # Step 2: Throttle MEDIUM priority if needed
    cur.execute("""
        UPDATE sensor_data
        SET state='THROTTLED', power_kw = power_kw * 0.7
        WHERE machine_id IN (
            SELECT machine_id FROM machines WHERE priority='MEDIUM'
        )
    """)
    conn.commit()

    print("MEDIUM priority machines throttled.")

    conn.close()
