import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import KFold, cross_validate


# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

DESCRIPTOR_FILE = "data/processed/caco2_rdkit_features.csv"
MORGAN_FILE = "data/processed/caco2_morgan_fingerprints.csv"


# ---------------------------------------------------------
# Features
# ---------------------------------------------------------

DESCRIPTOR_FEATURES = [
    "MW",
    "LogP",
    "HBD",
    "HBA",
    "TPSA",
    "RotBonds",
    "Rings",
    "FractionCSP3",
]


# ---------------------------------------------------------
# Load data
# ---------------------------------------------------------

desc_df = pd.read_csv(DESCRIPTOR_FILE)
morgan_df = pd.read_csv(MORGAN_FILE)

y = desc_df["Y"].values

X_desc = desc_df[DESCRIPTOR_FEATURES].values

morgan_columns = [f"Bit_{i}" for i in range(2048)]
X_morgan = morgan_df[morgan_columns].values

X_combined = np.hstack([X_desc, X_morgan])


# ---------------------------------------------------------
# Model
# ---------------------------------------------------------

model = RandomForestRegressor(
    n_estimators=300,
    random_state=42,
    n_jobs=-1
)


# ---------------------------------------------------------
# Cross-validation
# ---------------------------------------------------------

cv = KFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)


def evaluate_model(name, X):

    scores = cross_validate(
        model,
        X,
        y,
        cv=cv,
        scoring={
            "r2": "r2",
            "rmse": "neg_root_mean_squared_error",
            "mae": "neg_mean_absolute_error",
        },
        n_jobs=-1
    )

    r2 = scores["test_r2"]
    rmse = -scores["test_rmse"]
    mae = -scores["test_mae"]

    print(f"\n===== {name} =====")

    print("\nR² scores:")
    print(r2)

    print("\nMean R²:", round(r2.mean(), 4))
    print("Std R² :", round(r2.std(), 4))

    print("\nRMSE scores:")
    print(rmse)

    print("\nMean RMSE:", round(rmse.mean(), 4))
    print("Std RMSE :", round(rmse.std(), 4))

    print("\nMAE scores:")
    print(mae)

    print("\nMean MAE:", round(mae.mean(), 4))
    print("Std MAE :", round(mae.std(), 4))

    return {
        "Model": name,
        "Mean_R2": r2.mean(),
        "Std_R2": r2.std(),
        "Mean_RMSE": rmse.mean(),
        "Std_RMSE": rmse.std(),
        "Mean_MAE": mae.mean(),
        "Std_MAE": mae.std(),
    }


# ---------------------------------------------------------
# Run comparisons
# ---------------------------------------------------------

results = []

results.append(
    evaluate_model(
        "RDKit Descriptors",
        X_desc
    )
)

results.append(
    evaluate_model(
        "Morgan Fingerprints",
        X_morgan
    )
)

results.append(
    evaluate_model(
        "Combined Descriptors + Morgan",
        X_combined
    )
)


# ---------------------------------------------------------
# Save results
# ---------------------------------------------------------

results_df = pd.DataFrame(results)

results_df.to_csv(
    "results/caco2_model_comparison.csv",
    index=False
)

print("\n\n===== MODEL COMPARISON SUMMARY =====")
print(results_df.to_string(index=False))

print(
    "\nSaved: results/caco2_model_comparison.csv"
)
