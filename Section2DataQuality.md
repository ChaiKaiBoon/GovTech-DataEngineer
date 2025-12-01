| Rule                                                                           | Dimension    | Justification                                                             |
|--------------------------------------------------------------------------------|--------------|---------------------------------------------------------------------------|
| NRIC format must be `^[STFG]\d{7}[A-Z]$`                                       | Validity     | Ensures the value adheres to required pattern.                            |
| `decision_date` must be in `YYYY-MM-DD`                                        | Conformity   | Checks compliance with required formatting standard.                      |
| `application_status` ∈ {"Pending", "Approved", "Rejected"}                     | Conformity   | Ensures field uses the controlled vocabulary.                             |
| ------------------------------------------------------------------------------ | ------------ | ------------------------------------------------------------------------- |
| `application_id` must be non-null                                              | Completeness | Identifier must always be present.                                        |
| `citizen_nric` must be non-null                                                | Completeness | Required field to identify applicant.                                     |
| `household_income` must be non-null and ≥ 0                                    | Validity     | Must be numeric and non-negative.                                         |
| `household_size` must be non-null and positive integer                         | Validity     | Negative or zero household size is impossible.                            |
| `requested_amount` must be non-null and ≥ 0                                    | Validity     | Must be a valid numeric value.                                            |
| `approved_amount` must be ≥ 0 OR null when Pending/Rejected                    | Consistency  | Approved amount must match application status.                            |
| Date fields (`application_date`) must be valid dates                           | Conformity   | Check formatting and parsability.                                         |
| All UUIDs in `application_id` must follow UUID v4 pattern                      | Validity     | Ensures the field follows technical requirements.                         |
| `application_id` must be unique                                                | Uniqueness   | Key identifier must not be duplicated.                                    |
| `grant_scheme_name` should match canonical names (case insensitive)            | Conformity   | Standardizes variations like “HEALTHCARE SUBSIDY” / “Healthcare Subsidy”. |
| `decision_date` must be ≥ `application_date` (no decisions before application) | Consistency  | Ensures logical consistency.                                              |
| `decision_date` should not be null if status is Approved/Rejected              | Completeness | Final decision must have a date.                                          |
| Application date must not be in the future                                     | Validity     | Cannot submit an application before today.                                |
| Freshness rule: decision must be made ≤ 90 days after application              | Timeliness   | Agency SLA for processing time.                                           |
