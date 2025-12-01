import pandas as pd

class DimensionalModelBuilder:
    def build_dim_taxpayer(self, cleaned_df):
        cols = ["taxpayer_id","nric","full_name","filing_status","residential_status","postal_code","housing_type","number_of_dependents","cpf_contributions_sgd","_dq_score","_dq_issues","_nric_flag","_postal_flag"]
        dim = cleaned_df[cols].drop_duplicates(subset=["taxpayer_id"]).reset_index(drop=True)
        dim = dim.rename(columns={
            "postal_code":"postal_code_raw",
            "cpf_contributions_sgd":"cpf_contributions"
        })
        return dim

    def build_dim_time(self, cleaned_df):
        df = cleaned_df.copy()
        df['filing_date'] = pd.to_datetime(df['filing_date'], errors='coerce')
        dim = df[['assessment_year','filing_date']].drop_duplicates().reset_index(drop=True)
        dim['filing_year'] = dim['filing_date'].dt.year
        dim['filing_month'] = dim['filing_date'].dt.month
        dim['filing_quarter'] = dim['filing_date'].dt.quarter
        dim['is_after_deadline'] = dim['filing_date'] >= pd.to_datetime(dim['assessment_year'].astype(int)+1, format='%Y')
        return dim

    def build_dim_location(self, cleaned_df):
        d = cleaned_df[['postal_code','housing_type']].drop_duplicates().reset_index(drop=True)
        d['postal_sector'] = d['postal_code'].astype(str).str.zfill(6).str[:2]
        return d.rename(columns={'postal_code':'postal_code_raw'})

    def build_dim_occupation(self, cleaned_df):
        occ = cleaned_df[['occupation']].drop_duplicates().reset_index(drop=True)
        occ['occupation_id'] = occ.index + 1
        return occ[['occupation_id','occupation']]

    def build_fact_tax_returns(self, cleaned_df, dim_taxpayer, dim_time, dim_location, dim_occupation):
        f = cleaned_df.copy()
        f = f.merge(dim_occupation, on='occupation', how='left')
        f['filing_date'] = pd.to_datetime(f['filing_date'], errors='coerce')
        fact_cols = [
            'taxpayer_id','occupation_id','assessment_year','filing_date','annual_income_sgd','total_reliefs_sgd','chargeable_income_sgd','tax_payable_sgd','tax_paid_sgd','_dq_score','_dq_issues','_nric_flag','_postal_flag','_filing_date_flag','_chargeable_calc_flag','_cpf_rule_flag'
        ]
        fact = f[fact_cols].reset_index(drop=True)
        return fact