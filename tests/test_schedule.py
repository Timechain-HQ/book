"""The issuance schedule and a note round-trip."""

from __future__ import annotations

import unittest

from reference.notes import create_output, open_output
from reference.pq import ML_KEM, generate
from reference.schedule import BASE_UNITS, REWARD, TICKER, TOKEN_NAME, blocks_per_day, issued, supply
from reference.vm import run


class ScheduleTests(unittest.TestCase):
    def test_ticker_and_daily_mint(self) -> None:
        self.assertEqual(TOKEN_NAME, "Timecoin")
        self.assertEqual(TICKER, "TIC")
        self.assertEqual(supply(0), 0)
        self.assertEqual(supply(6), 6 * REWARD)
        self.assertEqual(blocks_per_day(), 144)
        self.assertEqual(issued(144), 144 * 50 * BASE_UNITS)
        self.assertEqual(issued(6), 300 * BASE_UNITS)

    def test_note_opens_for_its_view_key(self) -> None:
        private, public = generate(ML_KEM)
        other, _public = generate(ML_KEM)
        note, spend = create_output(public, REWARD, b"tic")
        opened = open_output(note, private)
        self.assertIsNotNone(opened)
        assert opened is not None
        self.assertEqual(opened[0], spend)
        self.assertEqual(opened[1], b"tic")
        self.assertIsNone(open_output(note, other))

    def test_sstore_costs_five(self) -> None:
        _storage, payout, gas = run(
            [("PUSH", 0), ("PUSH", 4), ("SSTORE",), ("PUSH", 0), ("PAYOUT",), ("STOP",)],
            {},
            [],
            0,
        )
        self.assertEqual(payout, 0)
        self.assertEqual(gas, 9)
