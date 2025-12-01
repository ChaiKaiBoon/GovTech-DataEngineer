# Cloud Deployment Guide (AWS) — Step-by-step


## 1) Prep (local / GitHub)
- Push repo to GitHub.

## 2) S3 buckets
- Create 3 buckets (raw, staging, curated)

## 3) Container image
- Build Docker image and push to ECR.
```
aws ecr create-repository --repository-name tax-etl
aws ecr get-login-password | docker login --username AWS --password-stdin <account>.dkr.ecr.<region>.amazonaws.com
docker build -t tax-etl:latest .
docker tag tax-etl:latest <account>.dkr.ecr.<region>.amazonaws.com/tax-etl:latest
docker push <account>.dkr.ecr.<region>.amazonaws.com/tax-etl:latest
```

## 4) Run ETL (ECS Fargate)
- Create IAM task role with least privilege to read/write S3, write logs to CloudWatch, read secrets.
- Create ECS cluster and task definition (CPU/memory sized for your workload). Use a scheduled Task or EventBridge to trigger daily.

## 5) Scale & large-scale ETL
- For heavy ETL (large datasets), consider AWS Glue/EMR/Databricks.
- Use Glue jobs to run Spark transforms and write Parquet to staged S3.

## 6) Analytics
- Use AWS Glue Data Catalog and Athena to query parquet or load into Redshift (RA3 nodes) for heavy BI.

## 7) Security
- Restrict S3 access via IAM and Bucket Policies, encrypt with KMS, enable CloudTrail.
- Place compute in private subnets (no public IP). Use VPC endpoints for S3.

## 8) CI/CD
- GitHub Actions pipeline to build image, run tests, push to ECR and update ECS service/task definition (or deploy to EKS).

---