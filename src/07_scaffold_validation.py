import numpy as np
import pandas as pd

from rdkit import Chem
from rdkit.Chem.Scaffolds import MurckoScaffold

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    r2_score,
    mean_squared_error,
    mean_absolute_error,
)


# =========================================================
# Paths
# =========================================================

RAW_FILE = "data/raw/caco2_wang.csv"
DESCRIPTOR_FILE = "data/processed/caco2_rdkit_features.csv"
MORGAN_FILE = "data/processed/caco2_morgan_fingerprints.csv"

OUTPUT_FILE = "results/caco2_scaffold_validation.csv"


# =========================================================
# Features
# =========================================================

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


# =========================================================
# Load data
# =========================================================

raw_df = pd.read_csv(RAW_FILE)
desc_df = pd.read_csv(DESCRIPTOR_FILE)
morgan_df = pd.read_csv(MORGAN_FILE)


print("Raw dataset shape:", raw_df.shape)
print("Descriptor dataset shape:", desc_df.shape)
print("Morgan dataset shape:", morgan_df.shape)


# =========================================================
# Build feature matrix
# =========================================================

y = desc_df["Y"].values

X_desc = desc_df[DESCRIPTOR_FEATURES].values

morgan_columns = [f"Bit_{i}" for i in range(2048)]
X_morgan = morgan_df[morgan_columns].values

X_combined = np.hstack([X_desc, X_morgan])


# =========================================================
# Verify alignment
# =========================================================

if len(raw_df) != len(X_combined):
    raise ValueError(
        "Row count mismatch between raw data and feature matrices."
    )

if len(y) != len(X_combined):
    raise ValueError(
        "Row count mismatch between target and feature matrices."
    )


# =========================================================
# Extract molecular structures
# =========================================================

smiles = raw_df["Drug"].astype(str).values


def get_scaffold(smiles_string):
    """
    Generate the Bemis-Murcko scaffold for a molecule.
    Returns 'NO_SCAFFOLD' if no valid scaffold can be generated.
    """

    mol = Chem.MolFromSmiles(smiles_string)

    if mol is None:
        return "INVALID"

    scaffold = MurckoScaffold.GetScaffoldForMol(mol)

    if scaffold is None or scaffold.GetNumAtoms() == 0:
        return "NO_SCAFFOLD"

    return Chem.MolToSmiles(scaffold)


scaffolds = np.array([
    get_scaffold(s)
    for s in smiles
])


# =========================================================
# Scaffold statistics
# =========================================================

unique_scaffolds = np.unique(scaffolds)

print("\n===== SCAFFOLD SUMMARY =====")

print("Total molecules:", len(scaffolds))
print("Unique scaffolds:", len(unique_scaffolds))
print(
    "Molecules with invalid structures:",
    np.sum(scaffolds == "INVALID")
)
print(
    "Molecules without explicit scaffold:",
    np.sum(scaffolds == "NO_SCAFFOLD")
)


# =========================================================
# Scaffold holdout validation
#
# Each scaffold is kept entirely inside either the
# training or validation set.
#
# We use approximately 80% of scaffolds for training
# and 20% for validation.
# =========================================================

rng = np.random.RandomState(42)

scaffold_list = list(unique_scaffolds)

rng.shuffle(scaffold_list)

n_train_scaffolds = int(0.80 * len(scaffold_list))

train_scaffolds = set(
    scaffold_list[:n_train_scaffolds]
)

test_scaffolds = set(
    scaffold_list[n_train_scaffolds:]
)


train_mask = np.array([
    scaffold in train_scaffolds
    for scaffold in scaffolds
])

test_mask = np.array([
    scaffold in test_scaffolds
    for scaffold in scaffolds
])


X_train = X_combined[train_mask]
X_test = X_combined[test_mask]

y_train = y[train_mask]
y_test = y[test_mask]


print("\n===== SCAFFOLD SPLIT =====")

print("Training molecules:", len(X_train))
print("Validation molecules:", len(X_test))

print("Training scaffolds:", len(train_scaffolds))
print("Validation scaffolds:", len(test_scaffolds))


# =========================================================
# Verify scaffold separation
# =========================================================

overlap = train_scaffolds.intersection(test_scaffolds)

if len(overlap) != 0:
    raise ValueError(
        "Scaffold leakage detected: "
        "some scaffolds occur in both training and validation."
    )

print("Scaffold overlap:", len(overlap))
print("Scaffold leakage check: PASSED")


# =========================================================
# Random Forest model
# =========================================================

model = RandomForestRegressor(
    n_estimators=300,
    random_state=42,
    n_jobs=-1
)


# =========================================================
# Train
# =========================================================

print("\nTraining Random Forest...")

model.fit(
    X_train,
    y_train
)


# =========================================================
# Predict
# =========================================================

y_pred = model.predict(X_test)


# =========================================================
# Performance
# =========================================================

r2 = r2_score(y_test, y_pred)

rmse = np.sqrt(
    mean_squared_error(y_test, y_pred)
)

mae = mean_absolute_error(
    y_test,
    y_pred
)

residuals = y_test - y_pred


print("\n===== SCAFFOLD VALIDATION RESULTS =====")

print("R²   :", round(r2, 4))
print("RMSE :", round(rmse, 4))
print("MAE  :", round(mae, 4))

print("\nResidual mean:", round(residuals.mean(), 4))
print("Residual std :", round(residuals.std(), 4))


# =========================================================
# Save results
# =========================================================

results = pd.DataFrame({
    "Validation": ["Scaffold Holdout"],
    "Training_Molecules": [len(X_train)],
    "Validation_Molecules": [len(X_test)],
    "Training_Scaffolds": [len(train_scaffolds)],
    "Validation_Scaffolds": [len(test_scaffolds)],
    "R2": [r2],
    "RMSE": [rmse],
    "MAE": [mae],
    "Residual_Mean": [residuals.mean()],
    "Residual_Std": [residuals.std()],
})


results.to_csv(
    OUTPUT_FILE,
    index=False
)


print("\nSaved:", OUTPUT_FILE)
