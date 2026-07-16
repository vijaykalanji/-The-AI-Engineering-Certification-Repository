# Payments team review checklist

- Verify retry backoff does not create duplicate charges.
- Confirm idempotency keys are preserved across retries.
- Ensure payment error codes map to user-safe messages.
- Require tests for timeout and partial-failure paths.
- Flag any schema change that affects ledger consistency.
