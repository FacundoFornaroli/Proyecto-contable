# scripts/etl_bank.py

from pathlib import Path
from typing import Union

import pandas as pd


def _read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, dtype=str)


def _read_excel(path: Path) -> pd.DataFrame:
    return pd.read_excel(path, engine="openpyxl", dtype=str)


def load_bank_statement(path: Union[str, Path]) -> pd.DataFrame:
    """
    Carga un extracto bancario en bruto (CSV o Excel).
    Si el DataFrame resultante tiene una sola columna, se separa usando el delimitador detectado.
    """
    path = Path(path)
    if path.suffix.lower() == ".csv":
        df_raw = _read_csv(path)
    else:
        df_raw = _read_excel(path)

    # Si solo hay una columna, separamos en múltiples
    if df_raw.shape[1] == 1:
        col = df_raw.columns[0]
        sample = df_raw.iloc[0, 0] or ""
        # detectamos si usa coma o punto y coma
        delim = "," if "," in sample else ";" if ";" in sample else None
        if delim is None:
            raise ValueError("No se detecta delimitador en la columna única")
        df = df_raw[col].str.split(delim, expand=True)
        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
        df.columns = [
            "date", "DrCr", "amount", "balance",
            "mode", "name", "Day", "Month", "Year", "Tday"
        ]
    else:
        df = df_raw.copy()
        # limpiar espacios en todos los valores string
        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    return df


def _parse_date(df: pd.DataFrame) -> pd.DataFrame:
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    return df



def _parse_amounts(df: pd.DataFrame) -> pd.DataFrame:
    df["amount"] = (
        df["amount"]
        .astype(str)
        .str.replace(r"[^\d\.]", "", regex=True)
        .astype(float)
    )
    df["balance"] = (
        df["balance"]
        .astype(str)
        .str.replace(r"[^\d\.]", "", regex=True)
        .astype(float)
    )
    return df


def clean_bank_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = _parse_date(df)
    df = _parse_amounts(df)
    # Aseguramos que 'amount' sea positivo
    df["amount"] = df["amount"].abs()
    return df[["date", "amount", "balance", "mode", "name"]]


if __name__ == "__main__":
    import sys

    default = Path("data_raw/bankstatements.xlsx")
    input_path = Path(sys.argv[1]) if len(sys.argv) > 1 else default

    if not input_path.exists():
        print(f"ERROR: no encuentro el archivo en {input_path}")
        sys.exit(1)

    raw_df = load_bank_statement(input_path)
    print(raw_df["date"].head(10).tolist())
    clean_df = clean_bank_df(raw_df)
    print(clean_df.head())
# Guarda el resultado limpio en carpeta data_processed
output_path = Path("data_processed/bank_clean.csv")
clean_df.to_csv(output_path, index=False)
print(f"\nArchivo guardado en: {output_path.resolve()}")


