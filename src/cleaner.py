import pandas as pd

class CleanerTransformer:
    def __init__(self, validator):
        self.v = validator

    def clean_row(self, row):
        r = row.copy()
        issues = []
        scores = 100
        nric_ok, nric_msg = self.v.validate_nric(r.get('nric'))
        r['_nric_valid'] = nric_ok
        r['_nric_flag'] = nric_msg
        if not nric_ok:
            issues.append(('nric', nric_msg)); scores -= 20
        pc_ok, pc_msg = self.v.validate_postal(r.get('postal_code'))
        r['_postal_valid'] = pc_ok
        r['_postal_flag'] = pc_msg
        if not pc_ok:
            issues.append(('postal_code', pc_msg)); scores -= 10
        fd_ok, fd_msg = self.v.validate_filing_date(r.get('filing_date'), int(r.get('assessment_year')))
        r['_filing_date_valid'] = fd_ok
        r['_filing_date_flag'] = fd_msg
        if not fd_ok:
            issues.append(('filing_date', fd_msg)); scores -= 15
        cq_ok, cq_msg = self.v.validate_chargeable_income_calc(r.get('annual_income_sgd',0), r.get('total_reliefs_sgd',0), r.get('chargeable_income_sgd',0))
        r['_chargeable_calc_valid'] = cq_ok
        r['_chargeable_calc_flag'] = cq_msg
        if not cq_ok:
            issues.append(('chargeable_income_calc', cq_msg)); scores -= 20
        cpf_ok, cpf_msg = self.v.validate_cpf_resident_rule(r.get('residential_status'), r.get('cpf_contributions_sgd',0))
        r['_cpf_rule_valid'] = cpf_ok
        r['_cpf_rule_flag'] = cpf_msg
        if not cpf_ok:
            issues.append(('cpf_rule', cpf_msg)); scores -= 10
        for f in ['full_name','occupation','housing_type','residential_status']:
            if pd.notna(r.get(f)):
                r[f] = str(r[f]).strip()
        numeric_cols = ['annual_income_sgd','chargeable_income_sgd','tax_payable_sgd','tax_paid_sgd','total_reliefs_sgd','cpf_contributions_sgd','foreign_income_sgd']
        for nc in numeric_cols:
            try:
                r[nc] = float(r.get(nc)) if pd.notna(r.get(nc)) and str(r.get(nc))!='' else None
            except Exception:
                r[nc] = None
        try:
            r['filing_date'] = pd.to_datetime(r.get('filing_date'), format=self.v.config['date_format'], errors='coerce')
        except Exception:
            r['filing_date'] = pd.NaT
        r['_dq_score'] = max(0, scores)
        r['_dq_issues'] = ';'.join([f"{k}:{v}" for k,v in issues]) if issues else ''
        return r

    def transform(self, df):
        cleaned = df.apply(self.clean_row, axis=1, result_type='expand')
        return cleaned