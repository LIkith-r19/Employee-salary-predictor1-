import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split

DATA_PATH = Path(__file__).resolve().parents[1] / "employee_data.csv"
MODEL_DIR = Path(__file__).resolve().parents[1] / "model_artifacts"
MODEL_DIR.mkdir(exist_ok=True, parents=True)
MODEL_PATH = MODEL_DIR / "salary_model.pkl"
PREPROCESSOR_PATH = MODEL_DIR / "preprocessor.pkl"
METRICS_PATH = MODEL_DIR / "metrics.json"

def load_data(path: Path = DATA_PATH) -> pd.DataFrame:
    df = pd.read_csv(path)
    # Defensive clean-up
    df = df.dropna(subset=["Salary"])
    # Coerce Experience to numeric
    if not pd.api.types.is_numeric_dtype(df["Experience"]):
        df["Experience"] = pd.to_numeric(df["Experience"], errors="coerce")
    df = df.dropna(subset=["Experience"])
    df["Experience"] = df["Experience"].astype(int)
    return df

def train_model(force: bool=False):
    """Train model if not exists or force=True. Returns (model, preprocessor, metrics dict)."""
    import json
    if MODEL_PATH.exists() and PREPROCESSOR_PATH.exists() and not force:
        model = joblib.load(MODEL_PATH)
        preprocessor = joblib.load(PREPROCESSOR_PATH)
        with open(METRICS_PATH) as f:
            metrics = json.load(f)
        return model, preprocessor, metrics

    df = load_data()
    y = df["Salary"].values
    X = df.drop(columns=["Salary"])

    num_features = ["Experience"]
    cat_features = [c for c in X.columns if c not in num_features]

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), cat_features),
            ("num", "passthrough", num_features),
        ]
    )

    # Basic model - could gridsearch; keep quick for demo
    model = RandomForestRegressor(
        n_estimators=400,
        random_state=42,
        n_jobs=-1,
        max_depth=None,
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    pipe = Pipeline(steps=[("prep", preprocessor), ("rf", model)])
    pipe.fit(X_train, y_train)

    y_pred = pipe.predict(X_test)
    r2 = r2_score(y_test, y_pred)

    # Persist
    joblib.dump(pipe, MODEL_PATH)
    joblib.dump(preprocessor, PREPROCESSOR_PATH)
    metrics = {"r2": float(r2), "n_rows": int(len(df))}
    with open(METRICS_PATH, "w") as f:
        json.dump(metrics, f, indent=2)

    return pipe, preprocessor, metrics

def load_or_train():
    return train_model(force=False)
