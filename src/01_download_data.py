from pathlib import Path

from tdc.single_pred import ADME


OUTPUT = Path("data/raw/caco2_wang.csv")


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    print("Downloading TDC Caco2_Wang dataset...")

    data = ADME(name="Caco2_Wang")
    df = data.get_data()

    df.to_csv(OUTPUT, index=False)

    print(f"Dataset saved: {OUTPUT}")
    print(f"Shape: {df.shape}")
    print("\nColumns:")
    print(df.columns.tolist())
    print("\nFirst five rows:")
    print(df.head())


if __name__ == "__main__":
    main()
