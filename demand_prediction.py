import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from load_balancer import apply_load_balancing



conn = sqlite3.connect("smart_grid.db")

query = """
SELECT 
    timestamp,
    SUM(power_kw) as total_load
FROM sensor_data
GROUP BY timestamp
ORDER BY timestamp
"""

df = pd.read_sql(query, conn)
conn.close()

df['timestamp'] = pd.to_datetime(df['timestamp'], format='ISO8601')

df.set_index('timestamp', inplace=True)

df['hour'] = df.index.hour
df['minute'] = df.index.minute

df['avg_5min'] = df['total_load'].rolling('5min').mean()
df['avg_10min'] = df['total_load'].rolling('10min').mean()

df['target_15min'] = df['total_load'].shift(-3)  # assuming 5-min intervals

df.dropna(inplace=True)


#LINEAR REGRESSION

X = df[['hour', 'minute', 'avg_5min', 'avg_10min']]
y = df['target_15min']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, shuffle=False
)

model = LinearRegression()
model.fit(X_train, y_train)

preds = model.predict(X_test)

mae = mean_absolute_error(y_test, preds)
print("Mean Absolute Error:", round(mae, 2), "kW")

def predict_next_15min(current_df):
    latest = current_df.iloc[-1]

    features = [[
        latest.name.hour,
        latest.name.minute,
        current_df['total_load'].rolling('5min').mean().iloc[-1],
        current_df['total_load'].rolling('10min').mean().iloc[-1]
    ]]

    return model.predict(features)[0]
predicted_load = preds[-1]
apply_load_balancing(predicted_load)

