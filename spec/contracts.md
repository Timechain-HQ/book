# Contracts

A contract account holds bytecode, an ML-DSA-44 capability key, a TIC balance, and integer storage. A call is valid only when that capability key signs the transaction sighash. There is no external call, so a contract cannot re-enter another contract.

```mermaid
flowchart TD
    arg{Argument 0}
    deposit[Call value must equal argument 1]
    add[Add argument 1 to slot 0 and to the TIC balance]
    withdraw[Call value is 0 and slot 0 covers argument 1]
    sub[Subtract argument 1 from slot 0 and pay it out]
    revert[Assert fails and the transaction is rejected]
    arg -->|1| deposit --> add
    arg -->|2| withdraw --> sub
    arg -->|other| revert
```

For a call:

```text
inputs = outputs + fee + callvalue - payout
```

`SSTORE` charges 5 gas. `STOP` charges nothing. The other completed opcodes charge 1. The gas limit is 10,000. A revert drops the whole transaction.

Transactions that do not share a note, a nullifier, or a contract id commute. Overlapping transactions stay in block order.

```mermaid
flowchart LR
    wave1[Wave of disjoint transactions]
    wave2[Next wave, after a shared note or contract]
    wave1 --> wave2
```
