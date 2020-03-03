# cro22-optin-design-seqanalysis
CRO22 email opt-in design test, sequential analysis

### During test

Run fetchdata and seqanalysis scripts daily / regularly, to monitor test progress.

### After test

1. Download SGLBL and RGLBL from SSRS
- Run lbl_munge to remove the PII
- Run lbl_ga_join to join with the GA data (linking transaction data to test cell buckets)
- Run tests to get the test statistics.