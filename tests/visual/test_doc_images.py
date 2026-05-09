from __future__ import annotations

import os
from pathlib import Path

import pytest
from playwright.sync_api import Page

from ha_testcontainer.visual import HA_SETTLE_MS, PAGE_LOAD_TIMEOUT

DOC_IMAGES = [
    {"id": "standard", "path": "0", "output": "docs/source/assets/images/standard.png"},
    {"id": "domains", "path": "0", "output": "docs/source/assets/images/domains.png"},
    {"id": "options", "path": "1", "output": "docs/source/assets/images/options.png"},
]
SETTLE_WAIT_MS = HA_SETTLE_MS * 2


def _write_or_verify(path: Path, image_bytes: bytes) -> None:
    update = os.environ.get("DOC_IMAGE_UPDATE") == "1"
    path.parent.mkdir(parents=True, exist_ok=True)
    if update or not path.exists():
        path.write_bytes(image_bytes)
        return
    expected = path.read_bytes()
    if expected != image_bytes:
        raise AssertionError(
            f"Documentation image changed: {path}. "
            "Re-run with DOC_IMAGE_UPDATE=1 to refresh docs images."
        )


@pytest.mark.parametrize("scenario", DOC_IMAGES, ids=[s["id"] for s in DOC_IMAGES])
def test_doc_image(scenario: dict[str, str], ha_page: Page, ha_url: str) -> None:
    ha_page.goto(
        f"{ha_url}/lovelace-yaml/{scenario['path']}",
        wait_until="networkidle",
        timeout=PAGE_LOAD_TIMEOUT,
    )
    ha_page.wait_for_timeout(SETTLE_WAIT_MS)

    image = ha_page.screenshot(full_page=True)
    _write_or_verify(Path(scenario["output"]), image)
