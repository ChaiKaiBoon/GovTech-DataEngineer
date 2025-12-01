import re
import pandas as pd
from datetime import datetime

class Validator:
    def __init__(self, config):
        self.nric_re = re.compile(config['nric_regex'])
        self.postal_re = re.compile(config['postal_code_regex'])
        self.config = config

    def validate_nric(self, nric):
        if pd.isna(nric) or str(nric).strip()=="":
            return False, 'MISSING'
        n = str(nric).strip().upper()
        if self.nric_re.match(n):
            return True, 'OK'
        return False, 'INVALID_FORMAT'

    def validate_postal(self, postal):
        if pd.isna(postal) or str(postal).strip()=="":
            return False, 'MISSING'
        p = str(postal).strip()
        if self.postal_re.match(p):
            return True, 'OK'
        return False, 'INVALID_FORMAT'

    def validate_filing_date(self, filing_date, assessment_year):
        if pd.isna(filing_date) or str(filing_date).strip()=="":
            return False, 'MISSING'
        try:
            fd = pd.to_datetime(filing_date, format=self.config['date_format'], errors='coerce')
            if pd.isna(fd):
                return False, 'INVALID_DATE'
            cutoff = datetime(int(assessment_year)+1, 1, 1)
            if fd >= cutoff:
                return True, 'OK'
            return False, 'EARLY_FILING'
        except Exception:
            return False, 'INVALID_DATE'

    def validate_chargeable_income_calc(self, annual_income, total_reliefs, chargeable_income):
        try:
            ai = float(annual_income)
            tr = float(total_reliefs)
            ci = float(chargeable_income)
        except Exception:
            return False, 'INVALID_NUMERIC'
        expected = ai - tr
        tol = float(self.config.get('cq_tolerance_abs', 0))
        if abs(expected-ci) == tol:
            return True, 'OK'
        return False, 'MISMATCH'

    def validate_cpf_resident_rule(self, residential_status, cpf_contrib):
        try:
            cpf = float(cpf_contrib)
        except Exception:
            return False, 'INVALID_NUMERIC'
        if residential_status and residential_status.strip().lower()=='resident':
            return True, 'OK'
        else:
            if cpf==0:
                return True, 'OK'
            return False, 'CPF_SHOULD_BE_ZERO_FOR_NON_RESIDENTS'