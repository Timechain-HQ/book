# Notes

A note carries a public amount and a one-time ML-DSA-44 spend key. ML-DSA-44 is FIPS 204, provided here by OpenSSL 3.5.

The recipient's long-term ML-KEM-768 view key stays off the chain. ML-KEM-768 is FIPS 203. The sender encapsulates to that view key, then encrypts the memo and the one-time spend key under the shared secret with an encrypt-then-MAC construction.

The commitment binds the amount, the one-time public key, a 32-byte rho, the ciphertext, and the MAC. The nullifier is derived from the one-time public key and rho. Publishing a nullifier spends the note once.

Conservation is public. The sum of spent notes equals the sum of new notes plus the fee, with contract deposits and payouts included. The fee is added to the coinbase. Supply increases only by the 50 TIME reward.
