import pandas as pd

# Replace these with your actual DataFrames
tcs_sales_df = ...
tcs_sales_return_df = ...
tax_invoice_details_df = ...

# Group and merge sales and return data
sales_grouped = tcs_sales_df.groupby('hsn_code').sum(numeric_only=True).reset_index()
returns_grouped = tcs_sales_return_df.groupby('hsn_code').sum(numeric_only=True).reset_index()

merged = pd.merge(sales_grouped, returns_grouped, on='hsn_code', how='left', suffixes=('', '_ret')).fillna(0)
merged['qty'] = merged['quantity'] - merged['quantity_ret']
merged['txval'] = merged['total_taxable_sale_value'] - merged['total_taxable_sale_value_ret']
merged['invval'] = merged['total_invoice_value'] - merged['total_invoice_value_ret']
merged['rt'] = merged['gst_rate']

# Create hsn_b2c list
hsn_b2c = []
for idx, row in merged.iterrows():
    camt = round(row['txval'] * row['rt'] / 200, 2)  # CGST
    samt = round(row['txval'] * row['rt'] / 200, 2)  # SGST
    iamt = 0
    hsn_b2c.append({
        "num": idx + 1,
        "hsn_sc": row['hsn_code'],
        "uqc": "PCS",
        "qty": row['qty'],
        "rt": row['rt'],
        "txval": row['txval'],
        "iamt": 0,
        "samt": 0,
        "camt": 0,
        "csamt": 0
    })

# Hardcoded B2B HSN (adjust as needed)
hsn_b2b = [{
    "num": 1,
    "hsn_sc": "7018",
    "uqc": "PCS",
    "qty": 0,
    "rt": 0,
    "txval": 0,
    "iamt": 0,
    "samt": 0,
    "camt": 0,
    "csamt": 0
}]

# Nil rated supplies
nil_inv = [
    {"sply_ty": "INTRB2B", "expt_amt": 0, "nil_amt": 0, "ngsup_amt": 0},
    {"sply_ty": "INTRAB2B", "expt_amt": 0, "nil_amt": 0, "ngsup_amt": 0},
    {"sply_ty": "INTRB2C", "expt_amt": 0, "nil_amt": 7080, "ngsup_amt": 0},
    {"sply_ty": "INTRAB2C", "expt_amt": 0, "nil_amt": 4269, "ngsup_amt": 0}
]

# E-commerce details
supeco = [{
    "etin": "09AARCM9332R1CM",
    "suppval": merged['txval'].sum(),
    "igst": 0,
    "cgst": 0,
    "sgst": 0,
    "cess": 0,
    "flag": "N"
}]

# Document summary
doc_det = []
for doc_type, group in tax_invoice_details_df.groupby('Type'):
    inv_sorted = sorted(group['Invoice No.'])
    doc_entry = {
        "doc_num": 1 if doc_type == "INVOICE" else 5,
        "doc_typ": doc_type,
        "docs": [{
            "num": 1,
            "from": inv_sorted[0],
            "to": inv_sorted[-1],
            "totnum": len(inv_sorted),
            "cancel": 0,
            "net_issue": len(inv_sorted)
        }]
    }
    doc_det.append(doc_entry)

# Final JSON structure
gstr1_json = {
    "gstin": "09KICPS3428C1Z4",
    "fp": "072025",
    "version": "GST3.1.6",
    "hash": "hash",
    "hsn": {
        "hsn_b2c": hsn_b2c,
        "hsn_b2b": hsn_b2b
    },
    "nil": {
        "inv": nil_inv
    },
    "supeco": {
        "clttx": supeco
    },
    "doc_issue": {
        "doc_det": doc_det
    }
}

# To save as JSON file:
import json
with open("gstr1.json", "w") as f:
    json.dump(gstr1_json, f, indent=4)

# Or print to console
print(json.dumps(gstr1_json, indent=4))
