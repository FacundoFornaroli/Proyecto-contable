# 🧾 Conciliación Contable Automatizada

Este proyecto tiene como objetivo automatizar el proceso de conciliación mensual entre extractos bancarios y comprobantes contables (facturas o pagos), utilizando Python para procesamiento y Power BI para visualización.

---

## 📌 Descripción del Proyecto

La conciliación contable es una tarea crítica en áreas de Finanzas y Administración. Este sistema permite detectar automáticamente:

- Transacciones bancarias **coincidentes** con comprobantes
- Movimientos bancarios **sin respaldo documental**
- Comprobantes **no cobrados** o pendientes de imputación

---

## ⚙️ Tecnologías Utilizadas

- **Python 3.9+**
  - `pandas` para procesamiento y limpieza de datos
  - `openpyxl` para lectura de archivos Excel
- **Power BI** para visualización interactiva
- Archivos de entrada: `.xlsx`, `.csv`

---

## 🧪 Estructura de Archivos

```bash
ProyContable/
├── data_raw/                  # Archivos originales
│   ├── bankstatements.xlsx
│   └── invoices.xlsx
├── data_processed/           # Resultados procesados
│   ├── bank_clean.csv
│   ├── invoices_clean.csv
│   ├── conciliados.csv
│   ├── banco_no_conciliado.csv
│   ├── facturas_no_conciliadas.csv
│   └── consolidado.csv
├── scripts/                  # Scripts principales
│   ├── etl_bank.py
│   ├── etl_invoices.py
│   └── reconciliation.py
└── dashboard.pbix            # (opcional) Dashboard en Power BI
