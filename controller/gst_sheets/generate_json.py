import pandas as pd
import json
import re

# ---------------- GST JSON Generator ----------------
def generate_json(sales_df, returns_df, invoice_df, gstin, fp, version="GST3.1.6"):
    # GST state codes
    gst_state_codes = {
        "jammu & kashmir":"01","himachal pradesh": "02", "punjab": "03", "chandigarh": "04",
        "uttarakhand": "05", "haryana": "06", "delhi": "07", "rajasthan": "08",
        "uttar pradesh": "09", "bihar": "10", "sikkim": "11", "arunachal pradesh": "12",
        "nagaland": "13", "manipur": "14", "mizoram": "15", "tripura": "16",
        "meghalaya": "17", "assam": "18", "west bengal": "19", "jharkhand": "20",
        "odisha": "21", "chhattisgarh": "22", "madhya pradesh": "23", "gujarat": "24",
        "daman and diu":"25","daman & diu":"25","dadra and nagar haveli":"26","dadra & nagar haveli":"26",
        "dadra and nagar haveli and daman and diu": "26", "maharashtra": "27",
        "andhra pradesh (old)": "28", "karnataka": "29", "goa": "30", "lakshadweep islands": "31",
        "kerala": "32", "tamil nadu": "33", "puducherry": "34", "andaman and nicobar islands": "35",
        "telangana": "36", "andhra pradesh": "37", "ladakh": "38","pondicherry": "34",
    }

    def get_state_code(state):
        if not isinstance(state, str): return None
        return gst_state_codes.get(state.strip().lower())

    supplier_state = gstin[:2]

    # ===== B2CS =====
    sales_group = sales_df.groupby(['gst_rate','end_customer_state_new'])[['total_taxable_sale_value','tax_amount']].sum().reset_index()
    returns_group = returns_df.groupby(['gst_rate','end_customer_state_new'])[['total_taxable_sale_value','tax_amount']].sum().reset_index()
    returns_group.rename(columns={'total_taxable_sale_value':'returns_txval','tax_amount':'returns_iamt'}, inplace=True)

    merged = pd.merge(sales_group, returns_group, how='left', on=['gst_rate','end_customer_state_new']).fillna(0)
    merged['net_txval'] = merged['total_taxable_sale_value'] - merged['returns_txval']
    merged['net_iamt'] = merged['tax_amount'] - merged['returns_iamt']

    b2cs_list = []
    for _, row in merged.iterrows():
        state_code = get_state_code(row['end_customer_state_new'])
        if not state_code: continue

        txval = round(row['net_txval'],2)
        rt = int(row['gst_rate'])
        tax_amt = round(row['net_iamt'],2)

        if state_code == supplier_state:
            camt = round(tax_amt/2,2)
            samt = round(tax_amt/2,2)
            b2cs_list.append({
                "sply_ty":"INTRA","rt":rt,"typ":"OE","pos":state_code,
                "txval":txval,"camt":camt,"samt":samt,"csamt":0
            })
        else:
            b2cs_list.append({
                "sply_ty":"INTER","rt":rt,"typ":"OE","pos":state_code,
                "txval":txval,"iamt":tax_amt,"csamt":0
            })

    # ===== HSN =====
    sales_hsn = sales_df.groupby(['hsn_code','gst_rate']).agg({'quantity':'sum','total_taxable_sale_value':'sum','tax_amount':'sum'}).reset_index()
    returns_hsn = returns_df.groupby(['hsn_code','gst_rate']).agg({'quantity':'sum','total_taxable_sale_value':'sum','tax_amount':'sum'}).reset_index()
    returns_hsn.rename(columns={'quantity':'returns_qty','total_taxable_sale_value':'returns_txval','tax_amount':'returns_iamt'}, inplace=True)

    hsn_merged = pd.merge(sales_hsn, returns_hsn, how='left', on=['hsn_code','gst_rate']).fillna(0)
    hsn_merged['net_qty'] = hsn_merged['quantity'] - hsn_merged['returns_qty']
    hsn_merged['net_txval'] = hsn_merged['total_taxable_sale_value'] - hsn_merged['returns_txval']
    hsn_merged['net_iamt'] = hsn_merged['tax_amount'] - hsn_merged['returns_iamt']

    hsn_list = []
    for i, row in hsn_merged.iterrows():
        hsn_code = str(row['hsn_code']).split('.')[0]  # remove decimal if any
        txval = round(row['net_txval'],2)
        qty = int(row['net_qty'])
        rt = int(row['gst_rate'])
        iamt = round(row['net_iamt'],2)

        # Split tax based on intra/inter state dynamically
        # For now, assume all HSNs are INTRA, split equally
        camt = samt = round(iamt/2,2) if iamt >= 0 else 0

        # Special handling for negative/returns
        if iamt < 0:
            camt = samt = 0

        hsn_list.append({
            "num": i+1,
            "hsn_sc": hsn_code,
            "uqc":"PCS",
            "qty": qty,
            "rt": rt,
            "txval": txval,
            "iamt": iamt,
            "samt": samt,
            "camt": camt,
            "csamt":0
        })


    # ===== DOC ISSUE =====
    def sort_key(val):
        match = re.match(r"([a-zA-Z]+)(\d+)", str(val))
        if match:
            prefix, num = match.groups()
            return (prefix,int(num))
        return (val,0)

    doc_issue_list = []
    for doc_type, label in [("INVOICE","Invoices for outward supply"),("CREDIT NOTE","Credit Note")]:
        df = invoice_df[invoice_df['Type'].str.upper()==doc_type]
        if df.empty: continue
        invoices = sorted(df['Invoice No.'].dropna().unique(), key=sort_key)
        if not invoices: continue
        docs_detail = [{"num":1,"from":invoices[0],"to":invoices[-1],"totnum":len(invoices),"cancel":0,"net_issue":len(invoices)}]
        doc_issue_list.append({"doc_num":len(doc_issue_list)+1,"doc_typ":label,"docs":docs_detail})

    # ===== SUPECO =====
    total_txval = sum(item.get("txval",0) for item in b2cs_list)
    total_iamt = sum(item.get("iamt",0) for item in b2cs_list)
    total_camt = sum(item.get("camt",0) for item in b2cs_list)
    total_samt = sum(item.get("samt",0) for item in b2cs_list)

    supeco_section = {
        "clttx":[
            {"etin":gstin,"suppval":round(total_txval,2),"igst":round(total_iamt,2),
             "cgst":round(total_camt,2),"sgst":round(total_samt,2),"cess":0,"flag":"N"}
        ]
    }

    # ===== FINAL JSON =====
    gst_json = {
        "gstin": gstin,
        "fp": fp,
        "version": version,
        "hash":"hash",
        "b2cs": b2cs_list,
        "hsn":{"hsn_b2c":hsn_list},
        "supeco": supeco_section,
        "doc_issue":{"doc_det":doc_issue_list}
    }

    return gst_json