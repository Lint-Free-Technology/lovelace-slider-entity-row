from __future__ import annotations

import os
from pathlib import Path

import pytest
from playwright.sync_api import Page

from ha_testcontainer.visual import HA_SETTLE_MS, PAGE_LOAD_TIMEOUT

SCENARIOS = [
    {"id": "types", "path": "0", "name": "types.png"},
    {"id": "options", "path": "1", "name": "options.png"},
    {"id": "attributes", "path": "2", "name": "attributes.png"},
    {"id": "width", "path": "3", "name": "width.png"},
    {"id": "errors", "path": "4", "name": "errors.png"},
]


def _assert_snapshot(path: Path, image_bytes: bytes) -> None:
    update = os.environ.get("VISUAL_UPDATE") == "1"
    path.parent.mkdir(parents=True, exist_ok=True)
    if update or not path.exists():
        path.write_bytes(image_bytes)
        return
    expected = path.read_bytes()
    if expected != image_bytes:
        raise AssertionError(
            f"Visual snapshot changed: {path}. "
            "Re-run with VISUAL_UPDATE=1 to accept the new snapshot."
        )


@pytest.mark.parametrize("scenario", SCENARIOS, ids=[s["id"] for s in SCENARIOS])
def test_view_snapshot(scenario: dict[str, str], ha_page: Page, ha_url: str) -> None:
    ha_page.goto(
        f"{ha_url}/lovelace-yaml/{scenario['path']}",
        wait_until="networkidle",
        timeout=PAGE_LOAD_TIMEOUT,
    )
    ha_page.wait_for_timeout(HA_SETTLE_MS * 2)
    image = ha_page.screenshot(full_page=True)

    snapshot_path = (
        Path(__file__).resolve().parent
        / "snapshots"
        / scenario["name"]
    )
    _assert_snapshot(snapshot_path, image)
