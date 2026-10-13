# Blocks

A block header binds:

- parent id
- height
- slot
- transactions
- up to two uncle ids
- coinbase note
- proposer ML-DSA-44 public key
- state root

The proposer signs that binding. The state root covers unspent notes, spent nullifiers, and contract accounts.

Fork choice selects the chain with the greatest height. If two tips share a height, the smaller block id wins.

An uncle is a block that lost that choice. It must share the parent's parent and the parent's height. The citing block records the uncle. The uncle's transactions are not executed again.

Two transactions commute when their notes and contracts do not overlap. Overlapping transactions stay in the order written in the block.
