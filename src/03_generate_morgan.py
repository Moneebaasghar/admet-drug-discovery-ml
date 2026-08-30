import pandas as pd
import numpy as np

from rdkit import Chem
from rdkit.Chem import rdFingerprintGenerator


INPUT = "data/raw/caco2_wang.csv"
OUTPUT = "data/processed/caco2_morgan_fingerprints.csv"

N_BITS = 2048
RADIUS = 2


def main():
    df = pd.read_csv(INPUT)

    molecules = df["Drug"].apply(Chem.MolFromSmiles)

    invalid = molecules.isna().sum()

    print(f"Total molecules: {len(molecules)}")
    print(f"Valid SMILES: {len(molecules) - invalid}")
    print(f"Invalid SMILES: {invalid}")

    if invalid > 0:
        raise ValueError("Invalid SMILES detected.")

    generator = rdFingerprintGenerator.GetMorganGenerator(
        radius=RADIUS,
        fpSize=N_BITS
    )

    fingerprints = []

    for mol in molecules:
        fp = generator.GetFingerprintAsNumPy(mol)
        fingerprints.append(fp)

    fingerprints = np.array(fingerprints, dtype=np.uint8)

    columns = [f"Bit_{i}" for i in range(N_BITS)]

    fp_df = pd.DataFrame(
        fingerprints,
        columns=columns
    )

    fp_df.insert(0, "Drug_ID", df["Drug_ID"].values)

    fp_df["Y"] = df["Y"].values

    fp_df.to_csv(OUTPUT, index=False)

    print(f"\nMorgan fingerprint matrix: {fingerprints.shape}")
    print(f"Saved: {OUTPUT}")
    print("Example first 20 bits:")
    print(fingerprints[0][:20])


if __name__ == "__main__":
    main()
