import pandas as pd
import numpy as np
import re
import csv
from datetime import datetime

# ----------------------------
# LOAD SAMPLE DATA
# ----------------------------

df = pd.read_csv('grant_applications.csv')
# ----------------------------
# RULE CHECKING FUNCTIONS
# ----------------------------

def is_valid_nric(nric):
    if pd.isna(nric):
        return False
    return bool(re.match(r"^[STFG]\d{7}[A-Z]$", str(nric)))

def is_valid_date_yyyy_mm_dd(x):
    try:
        datetime.strptime(str(x), "%Y-%m-%d")
        return True
    except:
        return False

def is_valid_date_any(x):
    try:
        pd.to_datetime(x, errors="raise")
        return True
    except:
        return False

def is_valid_uuid(u):
    return bool(re.match(r"^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$", str(u)))

# ----------------------------
# APPLY RULES PER DIMENSION
# ----------------------------

rules = {
    "Completeness": {
        "application_id_non_null": df["application_id"].notna(),
        "citizen_nric_non_null": df["citizen_nric"].notna(),
        "decision_date_required_for_final": ((df["application_status"].isin(["Approved", "Rejected"]) & df["decision_date"].notna()) |
                                             (~df["application_status"].isin(["Approved","Rejected"])))
    },
    "Uniqueness": {
        "application_id_unique": ~df["application_id"].duplicated()
    },
    "Validity": {
        "nric_format": df["citizen_nric"].apply(is_valid_nric),
        "income_valid": (df["household_income"] >= 0),
        "household_size_valid": (df["household_size"] > 0),
        "requested_amount_valid": df["requested_amount"] >= 0,
        "uuid_valid": df["application_id"].apply(is_valid_uuid)
    },
    "Conformity": {
        "decision_date_format": df["decision_date"].apply(is_valid_date_yyyy_mm_dd),
        "application_status_enum": df["application_status"].isin(["Pending","Approved","Rejected"]),
        "application_date_valid_format": df["application_date"].apply(is_valid_date_any),
        "canonical_grant_name": df["grant_scheme_name"].str.lower().isin(
            ["healthcare subsidy","education bursary","skills upgrading grant"]
        )
    },
    "Consistency": {
        "decision_after_application": [
            False if (not is_valid_date_any(df.loc[i,"application_date"]) or not is_valid_date_any(df.loc[i,"decision_date"]))
            else pd.to_datetime(df.loc[i,"decision_date"]) >= pd.to_datetime(df.loc[i,"application_date"])
            for i in df.index
        ],
        "approved_amount_logic": [
            (pd.isna(df.loc[i,"approved_amount"]) if df.loc[i,"application_status"]!="Approved"
             else df.loc[i,"approved_amount"]>=0)
            for i in df.index
        ]
    },
    "Timeliness": {
        "decision_within_90_days": [
            False if (not is_valid_date_any(df.loc[i,"application_date"]) or not is_valid_date_any(df.loc[i,"decision_date"]))
            else (pd.to_datetime(df.loc[i,"decision_date"]) - pd.to_datetime(df.loc[i,"application_date"])).days <= 90
            for i in df.index
        ]
    }
}

# ----------------------------
# CALCULATE DIMENSION SCORES
# ----------------------------

rows = len(df)
results = []

for dim, dim_rules in rules.items():
    rule_df = pd.DataFrame(dim_rules)
    passed = rule_df.all(axis=1).sum()
    score = round((passed / rows) * 100, 2)

    results.append({
        "dimension_name": dim,
        "score": score,
        "total_rows": rows,
        "rows_passed_all_rules": passed,
        "num_rules_in_dimension": len(dim_rules)
    })

dq_results = pd.DataFrame(results)

print(dq_results)
