import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import joblib

np.random.seed(42)

data = pd.DataFrame({
    "voltage": np.random.randint(210, 240, 1000),
    "current": np.random.uniform(5, 15, 1000),
    "temperature": np.random.uniform(30, 80, 1000)
})

data["power"] = data["voltage"] * data["current"]

model = IsolationForest(
    contamination=0.05,
    random_state=42
)

model.fit(data)

joblib.dump(model, "ml/anomaly_model.pkl")

print("Model trained and saved!")