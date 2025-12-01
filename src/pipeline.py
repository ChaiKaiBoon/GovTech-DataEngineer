import argparse
import pandas as pd
from pathlib import Path
from validators import Validator
from cleaner import CleanerTransformer
from builder import DimensionalModelBuilder
import yaml


def load_config(path='config.yml'):
    with open(path) as f:
        return yaml.safe_load(f)


class PipelineCLI:
    def __init__(self, config):
        self.config = config
        self.validator = Validator(config)
        self.cleaner = CleanerTransformer(self.validator)
        self.builder = DimensionalModelBuilder()

    def run(self, input_csv, output_dir):
        df = pd.read_csv(input_csv, dtype=str)
        # basic fill for numeric string columns
        for c in ["annual_income_sgd","total_reliefs_sgd","chargeable_income_sgd","cpf_contributions_sgd","tax_payable_sgd","tax_paid_sgd"]:
            if c in df.columns:
                df[c] = df[c].fillna("0")
        cleaned = self.cleaner.transform(df)
        dim_taxpayer = self.builder.build_dim_taxpayer(cleaned)
        dim_time = self.builder.build_dim_time(cleaned)
        dim_location = self.builder.build_dim_location(cleaned)
        dim_occupation = self.builder.build_dim_occupation(cleaned)
        fact_tax_returns = self.builder.build_fact_tax_returns(cleaned, dim_taxpayer, dim_time, dim_location, dim_occupation)
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)
        dim_taxpayer.to_csv(out / "dim_taxpayer.csv", index=False)
        dim_time.to_csv(out / "dim_time.csv", index=False)
        dim_location.to_csv(out / "dim_location.csv", index=False)
        dim_occupation.to_csv(out / "dim_occupation.csv", index=False)
        fact_tax_returns.to_csv(out / "fact_tax_returns.csv", index=False)
        print("Artifacts written to:", out)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--config', default='config.yml')
    args = parser.parse_args()
    cfg = load_config(args.config)
    p = PipelineCLI(cfg)
    p.run(args.input, args.output)