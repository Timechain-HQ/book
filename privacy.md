# Privacy

| Data | Who can see it |
| --- | --- |
| Amount and fee | Every node |
| Spent note | Every node, through the commitment and the nullifier |
| Long-term view key | The wallet that holds it |
| Memo and one-time spend key | The view key that can open the ciphertext |
| Capability key | Every node, on a contract call that uses it |
| Proposer key | Every node |

A sweep spends a received note into a fresh note encrypted to the same wallet. The previous sender's view key cannot open the swept note.

This is not complete privacy. Amounts and the path from one note to the next stay public so every node can reject an inflated transaction.
