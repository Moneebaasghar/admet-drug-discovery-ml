import os
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem.Draw import rdMolDraw2D

# ============================================================
# Configuration
# ============================================================

INPUT = "results/morgan_bit_analysis/final_morgan_chemical_environments.csv"

OUTPUT_DIR = "results/morgan_bit_visualizations"

TARGET_BITS = [623, 82, 1290, 550]

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================
# Load chemical-environment table
# ============================================================

df = pd.read_csv(INPUT)

print("Loaded:", df.shape)
print("Columns:", df.columns.tolist())

# ============================================================
# Helper: get Morgan environment atoms
# ============================================================

def get_environment_atoms(mol, atom_idx, radius):
    """
    Return the atom indices belonging to the Morgan environment
    centered on atom_idx with the specified radius.
    """

    bit_info = {}

    # Generate Morgan fingerprint only to recover atom environment
    from rdkit.Chem import rdFingerprintGenerator

    generator = rdFingerprintGenerator.GetMorganGenerator(
        radius=radius,
        fpSize=2048
    )

    generator.GetFingerprint(mol, additionalOutput=None)

    # Use RDKit's environment helper
    env = Chem.FindAtomEnvironmentOfRadiusN(
        mol,
        radius,
        atom_idx
    )

    atoms = {atom_idx}

    for bond_idx in env:
        bond = mol.GetBondWithIdx(bond_idx)
        atoms.add(bond.GetBeginAtomIdx())
        atoms.add(bond.GetEndAtomIdx())

    return sorted(atoms)


# ============================================================
# Draw each key Morgan bit
# ============================================================

for bit in TARGET_BITS:

    rows = df[df["Bit"] == f"Bit_{bit}"].copy()

    if rows.empty:
        print(f"\nWARNING: Bit {bit} not found.")
        continue

    # Use first representative molecule
    row = rows.iloc[0]

    drug_id = row["Drug_ID"]
    smiles = row["SMILES"]
    atom_idx = int(row["Atom_Index"])
    radius = int(row["Radius"])

    print("\n" + "=" * 60)
    print(f"Bit: {bit}")
    print(f"Drug ID: {drug_id}")
    print(f"Atom index: {atom_idx}")
    print(f"Radius: {radius}")

    mol = Chem.MolFromSmiles(smiles)

    if mol is None:
        print("ERROR: Could not parse SMILES.")
        continue

    # Generate 2D coordinates
    Chem.rdDepictor.Compute2DCoords(mol)

    # Find atoms belonging to Morgan environment
    highlight_atoms = get_environment_atoms(
        mol,
        atom_idx,
        radius
    )

    # Find bonds connecting highlighted atoms
    highlight_bonds = []

    for bond in mol.GetBonds():

        begin = bond.GetBeginAtomIdx()
        end = bond.GetEndAtomIdx()

        if begin in highlight_atoms and end in highlight_atoms:
            highlight_bonds.append(bond.GetIdx())

    # Draw
    drawer = rdMolDraw2D.MolDraw2DCairo(
        1200,
        900
    )

    drawer.drawOptions().addAtomIndices = False

    drawer.DrawMolecule(
        mol,
        highlightAtoms=highlight_atoms,
        highlightBonds=highlight_bonds
    )

    drawer.FinishDrawing()

    image = drawer.GetDrawingText()

    output = os.path.join(
        OUTPUT_DIR,
        f"morgan_bit_{bit}_final.png"
    )

    with open(output, "wb") as f:
        f.write(image)

    print(f"Saved: {output}")

print("\nAll requested Morgan-bit visualizations completed.")
