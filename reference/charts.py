"""Charts computed from the issuance schedule and the reference machine."""

from __future__ import annotations

from pathlib import Path

from reference.notes import create_output
from reference.pngchart import INK, PAPER, Canvas, bar_chart, composition_chart, fork_chart, line_chart
from reference.pq import ML_KEM, generate
from reference.schedule import (
    BASE_UNITS,
    REWARD,
    SLOT_TARGET_SECONDS,
    TICKER,
    blocks_per_day,
    blocks_per_hour,
    issued,
    supply,
)
from reference.vm import Step, run


def write_charts(directory: str | Path) -> dict[str, int]:
    path = Path(directory)
    path.mkdir(parents=True, exist_ok=True)
    day = blocks_per_day()
    heights = list(range(0, day + 1, 12))
    line_chart(
        path / "supply.png",
        f"Supply if every block mints 50 {TICKER}",
        "height",
        TICKER,
        [("supply", [(height, supply(height) / BASE_UNITS) for height in heights])],
    )
    line_chart(
        path / "slots.png",
        "Seconds at the 600 second target",
        "height",
        "seconds",
        [("target", [(height, height * SLOT_TARGET_SECONDS) for height in heights])],
    )
    bar_chart(
        path / "issuance.png",
        f"{TICKER} minted when blocks hit the slot target",
        "window",
        ["block", "hour", "day"],
        [
            (
                TICKER,
                [
                    issued(1) / BASE_UNITS,
                    issued(blocks_per_hour()) / BASE_UNITS,
                    issued(day) / BASE_UNITS,
                ],
            )
        ],
    )
    costs = _opcode_costs()
    bar_chart(
        path / "opcode-gas.png",
        "Gas charged by one completed instruction",
        "opcode",
        [name for name, _cost in costs],
        [("gas", [float(cost) for _name, cost in costs])],
    )
    _view_private, view_pub = generate(ML_KEM)
    note, _spend = create_output(view_pub, REWARD, b"book")
    composition_chart(path / "note-bytes.png", "Measured bytes in a 50 TIC note", note.parts())
    _header(path / "header.png")
    _uncle_rule(path / "uncle-rule.png")
    paid = 100_000_000
    fee = 1_000
    bar_chart(
        path / "conservation.png",
        f"Input equals output plus fee, in {TICKER}",
        "part",
        ["input", "out+fee"],
        [(TICKER, [paid / BASE_UNITS, (paid - fee + fee) / BASE_UNITS])],
    )
    report = [
        "# Book charts",
        "",
        "Written by `python3 -m reference.charts`.",
        "",
        f"Token: Timecoin. Ticker: {TICKER}.",
        f"Reward: {REWARD} base units. Slot target: {SLOT_TARGET_SECONDS} seconds.",
        f"Blocks in a day at the target: {day}. Daily mint: {issued(day)} base units.",
        f"Hourly mint: {issued(blocks_per_hour())} base units.",
        f"Conservation example: {paid} = {paid - fee} + {fee}.",
        f"Note bytes: {sum(size for _name, size in note.parts())}.",
        "",
        "| Opcode | Gas |",
        "| --- | --- |",
    ]
    for name, cost in costs:
        report.append(f"| {name} | {cost} |")
    report.append("")
    (path / "README.md").write_text("\n".join(report), encoding="utf-8")
    return {"day": day, "daily": issued(day), "note_bytes": sum(size for _name, size in note.parts())}


def _opcode_costs() -> list[tuple[str, int]]:
    samples = [
        ("PUSH", [("PUSH", 1)], 0, [], 0),
        ("ADD", [("PUSH", 2), ("PUSH", 3), ("ADD",)], 2, [], 0),
        ("SUB", [("PUSH", 5), ("PUSH", 2), ("SUB",)], 2, [], 0),
        ("EQ", [("PUSH", 1), ("PUSH", 1), ("EQ",)], 2, [], 0),
        ("GE", [("PUSH", 3), ("PUSH", 1), ("GE",)], 2, [], 0),
        ("ASSERT", [("PUSH", 1), ("ASSERT",)], 1, [], 0),
        ("ARG", [("ARG", 0)], 0, [7], 0),
        ("CALLVALUE", [("CALLVALUE",)], 0, [], 4),
        ("SLOAD", [("PUSH", 0), ("SLOAD",)], 1, [], 0),
        ("SSTORE", [("PUSH", 1), ("PUSH", 9), ("SSTORE",)], 2, [], 0),
        ("PAYOUT", [("PUSH", 0), ("PAYOUT",)], 1, [], 0),
        ("SWAP", [("PUSH", 1), ("PUSH", 2), ("SWAP",)], 2, [], 0),
        ("JUMPI", [("PUSH", 0), ("JUMPI", 0)], 1, [], 0),
        ("JUMP", [("JUMP", 1), ("STOP",)], 0, [], 0),
        ("STOP", [("STOP",)], 0, [], 0),
    ]
    measured: list[tuple[str, int]] = []
    for name, code, index, args, callvalue in samples:
        steps: list[Step] = []
        run(code, {}, args, callvalue, steps=steps)
        previous = 0 if index == 0 else steps[index - 1].gas_used
        measured.append((name, steps[index].gas_used - previous))
    return measured


def _header(path: Path) -> None:
    canvas = Canvas(960, 680)
    canvas.text(24, 16, "FIELDS COVERED BY THE BLOCK SIGNATURE", INK, 2)
    fields = [
        "NETWORK AND CHAIN ID",
        "PARENT HASH",
        "HEIGHT AND SLOT",
        "TRANSACTIONS",
        "UNCLE HASHES, AT MOST 2",
        "COINBASE NOTE",
        "PROPOSER ML-DSA PUBLIC KEY",
        "STATE ROOT",
        "ML-DSA SIGNATURE IS OUTSIDE THE SIGNED BYTES",
    ]
    y = 58
    for field in fields:
        canvas.rect(32, y, 896, 58, PAPER)
        canvas.frame(32, y, 896, 58, INK, 2)
        canvas.text(48, y + 18, field, INK, 2)
        y += 66
    canvas.save(path)


def _uncle_rule(path: Path) -> None:
    fork_chart(
        path,
        "Uncle rule: cite a sibling of the parent",
        [
            {"label": "Grandparent", "detail": "shared", "column": 1, "row": 0, "kind": "genesis"},
            {"label": "Parent", "detail": "extended", "column": 0, "row": 1, "kind": "canonical", "parent": (1, 0)},
            {"label": "Uncle", "detail": "same height", "column": 2, "row": 1, "kind": "uncle", "parent": (1, 0)},
            {
                "label": "Child",
                "detail": "may cite it",
                "column": 0,
                "row": 2,
                "kind": "canonical",
                "parent": (0, 1),
                "uncle": (2, 1),
            },
        ],
    )


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    result = write_charts(root / "docs" / "charts")
    print(f"daily {result['daily']}  note {result['note_bytes']}")


if __name__ == "__main__":
    main()
