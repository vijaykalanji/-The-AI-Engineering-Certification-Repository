"""Compute before/after percentile table for the certification writeup."""

from __future__ import annotations

import json
from pathlib import Path


def percentile(values: list[float], p: float) -> float:
    # TODO: implement percentile (sort + index or statistics.quantiles)
    raise NotImplementedError


def main() -> None:
    data = json.loads((Path(__file__).parent / "baseline_vs_treatment.json").read_text())
    # TODO: print markdown table for P50/P75/P90 Time In Review + stale rates
    print("Implement eval table printer using baseline_vs_treatment.json")


if __name__ == "__main__":
    main()
