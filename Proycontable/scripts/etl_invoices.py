# scripts/etl_invoices.py

from pathlib import Path
import pandas as pd


def load_invoices(path: Path) -> pd.DataFrame:
    if path.suffix.lower() == ".csv":
        df = pd.read_csv(path, dtype=str)
    else:
        df = pd.read_excel(path, engine="openpyxl", dtype=str)
    return df


def clean_invoices(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpia facturas o comprobantes para conciliación bancaria.
    Estándariza: date, amount, name y method → compatibles con extracto bancario.
    """
    df = df.copy()
    df.columns = [col.strip().lower() for col in df.columns]

    # Renombra columnas clave si vienen como client/supplier
    if "client" in df.columns:
        df.rename(columns={"client": "name"}, inplace=True)
    elif "supplier" in df.columns:
        df.rename(columns={"supplier": "name"}, inplace=True)

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["amount"] = (
        df["amount"]
        .astype(str)
        .str.replace(r"[^\d\.-]", "", regex=True)
        .astype(float)
        .abs()
    )

    df["name"] = df["name"].astype(str).str.strip().str.upper()

    if "method" in df.columns:
        df.rename(columns={"method": "mode"}, inplace=True)

    # Reordenar y seleccionar columnas compatibles con banco
    return df[["date", "amount", "mode", "name"]]


if __name__ == "__main__":
    import sys

    default = Path("data_raw/invoices.xlsx")
    input_path = Path(sys.argv[1]) if len(sys.argv) > 1 else default

    if not input_path.exists():
        print(f"ERROR: no encuentro el archivo en {input_path}")
        sys.exit(1)

    df_raw = load_invoices(input_path)
    df_clean = clean_invoices(df_raw)

    output_path = Path("data_processed/invoices_clean.csv")
    df_clean.to_csv(output_path, index=False)

    print(df_clean.head())
    print(f"\nArchivo limpio guardado en: {output_path.resolve()}")
