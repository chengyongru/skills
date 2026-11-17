# Make Operations Idempotent

Make state-changing operations converge to the correct state wherever the previous run stopped. Read current state, compare it with the goal, and apply only the difference instead of trusting the previous run's intent.

Make owned locks, temporary files, partial records, and claimed jobs reconcilable after a crash. Prove ownership and staleness from current process/artifact evidence, not timestamps alone; preserve unknown resources. Use atomic replacement for owned files where supported and keep external run state single-writer.

Test two consecutive runs and a crash at each meaningful boundary. If the answer depends on leftover state, add reconciliation. Idempotence does not authorize repeating an uncertain external effect: inspect the target/head and effect state, use a supported idempotency key where available, or stop rather than risk duplication. Authorization and requested schedules remain unchanged.
