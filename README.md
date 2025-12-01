CHAI KAI BOON Code
Background
A government agency needs to modernize their data analytics platform to support policy making, compliance monitoring, and revenue forecasting. As a Senior Data Engineer, you are tasked with building a robust, scalable data processing pipeline that can handle tax data while ensuring data quality, security, and analytical capabilities.

Task1
Main file: pipeline.py To run program - pipeline.py --input data/individual_tax_returns.csv --output outputs/

Task2
Step by step deployment: docs/cloud_deployment.md

Security Diagram

Simple diagram [User] | v [Repo] -- CI/CD --> [ECR] | v [ECS Fargate / EKS]
| +-------------------------+-------------------------+ | | | v v v [S3 - raw bucket] [S3 - staging/parquet] [S3 - curated] | | | v v v [AWS Glue / EMR / Spark] -> transform -> load -> [Redshift / Athena / Lake Formation / Glue Catalog] | v [BI Tools] (Looker/Quicksight/Tableau)

Security boundaries & practices
S3 buckets with least-privilege IAM roles (separate raw/staging/curated). VPC + private subnets for compute (ECS tasks / EMR) and Redshift. KMS encryption for S3 and Redshift. AWS Lake Formation or Glue Data Catalog for access control and data governance. Audit logs via CloudTrail and S3 access logs.

Why these services
S3 + Parquet + Glue is cost-effective and scalable. EKS/ECS for containerized jobs gives mature scheduling and scaling. Redshift/Athena for analytics and BI queries. IAM + KMS provides strong security controls required for government data.

Section 2 answers
Data Quality rules :Section2DataQuality

Data model diagram : Section2DataModel.md
