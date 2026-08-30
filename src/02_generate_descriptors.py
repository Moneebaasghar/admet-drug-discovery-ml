import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors, Lipinski, rdMolDescriptors

INPUT = "data/raw/caco2_wang.csv"
OUTPUT = "data/processed/caco2_rdkit_features.csv"

FEATURES = [
    "MW",
    "LogP",
    "HBD",
    "HBA",
    "TPSA",
    "RotBonds",
    "Rings",
    "FractionCSP3",
]


def main():
    df = pd.read_csv(INPUT)

    print(f"Input dataset: {df.shape}")

    molecules = df["Drug"].apply(Chem.MolFromSmiles)

    invalid = molecules.isna().sum()

    print(f"Valid SMILES: {len(molecules) - invalid}")
    print(f"Invalid SMILES: {invalid}")

    if invalid > 0:
        raise ValueError("Invalid SMILES detected.")

    df["MW"] = molecules.apply(Descriptors.MolWt)
    df["LogP"] = molecules.apply(Descriptors.MolLogP)
    df["HBD"] = molecules.apply(Lipinski.NumHDonors)
    df["HBA"] = molecules.apply(Lipinski.NumHAcceptors)
    df["TPSA"] = molecules.apply(rdMolDescriptors.CalcTPSA)
    df["RotBonds"] = molecules.apply(Lipinski.NumRotatableBonds)
    df["Rings"] = molecules.apply(rdMolDescriptors.CalcNumRings)
    df["FractionCSP3"] = molecules.apply(
        rdMolDescriptors.CalcFractionCSP3
    )

    output_columns = [
        "Drug_ID",
        "Drug",
        *FEATURES,
        "Y",
    ]

    result = df[output_columns]

    result.to_csv(OUTPUT, index=False)

    print("\n===== RDKit DESCRIPTORS =====")
    print(result.head().to_string(index=False))

    print(f"\nFeature dataset saved: {OUTPUT}")
    print(f"Shape: {result.shape}")


if __name__ == "__main__":
    main()
