# State

The token is Timecoin. The ticker is TIC. 1 TIC = 10^8 base units. Genesis supply is zero. Each applied block adds 50 TIC. A fee does not mint TIC. It leaves the spent notes and enters the coinbase.

```mermaid
flowchart TD
    parent[Parent state]
    txs[Apply transactions in listed order]
    conserve{Inputs equal outputs plus fee, adjusted for call value and payout}
    coin[Coinbase equals 50 TIC plus the fees]
    supply[Supply increases by 50 TIC]
    audit[Unspent notes plus contract balances equal supply]
    parent --> txs --> conserve
    conserve -->|no| reject[Reject the block]
    conserve -->|yes| coin --> supply --> audit
```

The state root is a Merkle root of three kinds of leaves:

- each unspent note, bound to its commitment and amount
- each published nullifier
- each contract account: code, capability key, TIC balance, and storage

A node stores the blocks and recomputes this root. A balance written into the block file is not state.
