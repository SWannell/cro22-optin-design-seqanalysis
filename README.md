# Prompt test: CRO22 email opt-in design test

Based on [the sequential analysis repo](https://github.com/britishredcrosssociety/sequential-analysis).

### During test

Run fetchdata and seqanalysis scripts daily / regularly, to monitor test progress.

### After test

1. Download SGLBL and RGLBL from SSRS
2. Run lbl_munge to remove the PII
3. Run lbl_ga_join to join with the GA data (linking transaction data to test cell buckets)
4. Run tests to get the test statistics.
