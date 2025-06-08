from pathlib import Path
import pandas as pd

# Carga de los archivos limpios
bank_df = pd.read_csv("data_processed/bank_clean.csv", parse_dates=["date"])
inv_df = pd.read_csv("data_processed/invoices_clean.csv", parse_dates=["date"])

# Normalizamos nombres y tipos
bank_df["name"] = bank_df["name"].astype(str).str.upper().str.strip()
inv_df["name"] = inv_df["name"].astype(str).str.upper().str.strip()

# Marcamos si están conciliados
bank_df["conciliado"] = False
inv_df["conciliado"] = False

matches = []

# Recorremos banco y buscamos coincidencias en facturas
for idx_b, row_b in bank_df.iterrows():
    posibles = inv_df[
        (~inv_df["conciliado"]) &
        (inv_df["amount"] == row_b["amount"]) &
        (inv_df["name"] == row_b["name"]) &
        (inv_df["date"].between(row_b["date"] - pd.Timedelta(days=3),
                                row_b["date"] + pd.Timedelta(days=3)))
    ]
    if not posibles.empty:
        idx_i = posibles.index[0]
        inv_df.at[idx_i, "conciliado"] = True
        bank_df.at[idx_b, "conciliado"] = True
        matches.append({
            "banco_fecha": row_b["date"],
            "factura_fecha": inv_df.at[idx_i, "date"],
            "nombre": row_b["name"],
            "monto": row_b["amount"]
        })

# Exportamos resultados
pd.DataFrame(matches).to_csv("data_processed/conciliados.csv", index=False)
bank_df[~bank_df["conciliado"]].to_csv("data_processed/banco_no_conciliado.csv", index=False)
inv_df[~inv_df["conciliado"]].to_csv("data_processed/facturas_no_conciliadas.csv", index=False)

print("✔ Conciliación completada.")
print(f"→ Conciliados: {len(matches)}")
print(f"→ Banco sin conciliar: {len(bank_df[~bank_df['conciliado']])}")
print(f"→ Facturas sin conciliar: {len(inv_df[~inv_df['conciliado']])}")
