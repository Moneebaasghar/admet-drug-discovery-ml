import os
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Draw

INPUT = "results/morgan_bit_analysis/final_morgan_chemical_environments.csv"
OUTPUT_DIR = "results/morgan_bit_visualizations"

TARGET_BITS = [623, 82, 1290, 550]

os.makedirs(OUTPUT_DIR, exist_ok=True)

df = pd.read_csv(INPUT)

for bit in TARGET_BITS:

    rows = df[df["Bit"] == f"Bit_{bit}"]

    if rows.empty:
        print(f"Bit {bit}: NOT FOUND")
        continue

    row = rows.iloc[0]

    mol = Chem.MolFromSmiles(row["SMILES"])

    atom_idx = int(row["Atom_Index"])
    radius = int(row["Radius"])

    if mol is None:
        print(f"Bit {bit}: invalid SMILES")
        continue

    # Exact Morgan environment
    env_bonds = Chem.FindAtomEnvironmentOfRadiusN(
        mol,
        radius,
        atom_idx
    )

    env_atoms = {atom_idx}

    for bond_idx in env_bonds:
        bond = mol.GetBondWithIdx(bond_idx)
        env_atoms.add(bond.GetBeginAtomIdx())
        env_atoms.add(bond.GetEndAtomIdx())

    env_atoms = sorted(env_atoms)

    print("\n" + "=" * 70)
    print(f"BIT {bit}")
    print(f"Drug ID: {row['Drug_ID']}")
    print(f"Center atom: {atom_idx}")
    print(f"Radius: {radius}")
    print(f"Environment atoms: {env_atoms}")
    print(f"Environment bonds: {list(env_bonds)}")

    # Highlight exact environment
    highlight_atoms = env_atoms
    highlight_bonds = list(env_bonds)

    # Draw
    img = Draw.MolToImage(
        mol,
        size=(1400, 1000),
        highlightAtoms=highlight_atoms,
        highlightBonds=highlight_bonds,
        kekulize=False
    )

    output = os.path.join(
        OUTPUT_DIR,
        f"morgan_bit_{bit}_EXACT.png"
    )

    img.save(output)

    print(f"Saved: {output}")

print("\nFinished all four exact Morgan environments.")
