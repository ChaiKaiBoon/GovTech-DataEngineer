┌──────────────────────────┐
│      data_quality_run     │
├──────────────────────────┤
│ run_id (PK)              │
│ run_timestamp            │
│ source_system            │
│ dataset_name             │
└───────────────┬──────────┘
                │1:N
┌──────────────────────────────────────────────┐
│         data_quality_dimension_score         │
├──────────────────────────────────────────────┤
│ score_id (PK)                                 │
│ run_id (FK)                                   │
│ dimension_name                                │
│ dimension_score                               │
│ total_rows                                    │
│ passed_rows                                   │
└───────────────┬──────────────────────────────┘
                │1:N
┌──────────────────────────────────────────────┐
│             data_quality_rule_result         │
├──────────────────────────────────────────────┤
│ rule_result_id (PK)                           │
│ score_id (FK)                                 │
│ rule_name                                     │
│ passed_count                                  │
│ failed_count                                  │
│ rule_description                              │
│ dimension_name                                │
└──────────────────────────────────────────────┘
