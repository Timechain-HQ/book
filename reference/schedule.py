"""Issuance arithmetic for the Timecoin token.

The ticker is TIC. A block that meets the slot target mints 50 TIC.
These functions are the schedule the charts draw.
"""

from __future__ import annotations

TOKEN_NAME = "Timecoin"
TICKER = "TIC"
BASE_UNITS = 10**8
REWARD = 50 * BASE_UNITS
SLOT_TARGET_SECONDS = 600


def supply(height: int) -> int:
    if height < 0:
        raise ValueError("height")
    return height * REWARD


def blocks_per_day() -> int:
    return 86_400 // SLOT_TARGET_SECONDS


def blocks_per_hour() -> int:
    return 3_600 // SLOT_TARGET_SECONDS


def issued(blocks: int) -> int:
    if blocks < 0:
        raise ValueError("blocks")
    return blocks * REWARD
