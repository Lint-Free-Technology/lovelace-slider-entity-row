from __future__ import annotations

import os
import shutil
import threading
from pathlib import Path
from typing import Any

import pytest
from ha_testcontainer import HATestContainer, HAVersion
import yaml

REPO_ROOT = Path(__file__).parent.parent
HA_CONFIG_DIR = REPO_ROOT / "tests" / "ha-config"
DIST_JS = REPO_ROOT / "dist" / "slider-entity-row.js"
HA_LOVELACE_VIEWS_DIR = HA_CONFIG_DIR / "lovelace" / "views"
HA_LOVELACE_URL_PATH = "lovelace"
HA_LOVELACE_VIEW_FILES = (
    "2_options.yaml",
    "3_attributes.yaml",
    "4_width.yaml",
    "5_errors.yaml",
)


@pytest.fixture(scope="session")
def ha_version() -> str:
    return os.environ.get("HA_VERSION", HAVersion.STABLE)


@pytest.fixture(scope="session")
def ha(ha_version: str, tmp_path_factory):
    if not DIST_JS.exists():
        raise RuntimeError(
            "dist/slider-entity-row.js is missing. Run `npm run build` before running visual tests."
        )

    ha_tmp = tmp_path_factory.mktemp("ha-state")
    shutil.copytree(str(HA_CONFIG_DIR), str(ha_tmp), dirs_exist_ok=True)

    container = HATestContainer(
        version=ha_version,
        config_path=ha_tmp,
    )
    container.with_volume_mapping(str(REPO_ROOT.resolve()), "/config/www/workspace", "rw")
    container.start()

    yield container
    container.stop()


@pytest.fixture(scope="session")
def ha_url(ha) -> str:
    return ha.get_url()


@pytest.fixture(scope="session")
def ha_token(ha) -> str:
    return ha.get_token()


def _run_ws_command(ha, command: dict[str, Any]) -> dict[str, Any]:
    """Run an HA websocket command with timeout handling."""
    result: dict[str, Any] = {}
    exc_holder: list[Exception] = []

    def _run() -> None:
        try:
            result.update(ha._ws_call(command))
        except Exception as exc:
            exc_holder.append(exc)

    thread = threading.Thread(target=_run, daemon=True)
    thread.start()
    thread.join(timeout=30)
    if thread.is_alive():
        raise TimeoutError(f"WebSocket command timed out: {command.get('type')}")
    if exc_holder:
        raise RuntimeError(
            f"WebSocket command failed: type={command.get('type')}, id={command.get('id')}"
        ) from exc_holder[0]
    return result


def _load_dashboard_views() -> list[dict[str, Any]]:
    """Load static Lovelace view YAML files into dashboard view dictionaries."""
    views: list[dict[str, Any]] = []
    for file_name in HA_LOVELACE_VIEW_FILES:
        data = yaml.safe_load((HA_LOVELACE_VIEWS_DIR / file_name).read_text())
        if not isinstance(data, dict):
            raise RuntimeError(
                f"Invalid Lovelace view format in {file_name}: expected dict, got {type(data).__name__}"
            )
        # x-anchors are YAML-only helper aliases and not valid Lovelace config keys.
        data.pop("x-anchors", None)
        views.append(data)
    return views


@pytest.fixture(scope="session")
def ha_lovelace_url_path(ha) -> str:
    views = _load_dashboard_views()
    result = _run_ws_command(
        ha,
        {
            "id": 1,
            "type": "lovelace/config/save",
            "config": {
                "title": "slider-entity-row",
                "views": views,
            },
        },
    )
    if not result.get("success"):
        error = result.get("error")
        raise RuntimeError(
            f"Failed to save Lovelace dashboard config via {result.get('type', 'lovelace/config/save')}: {error or result}"
        )
    return HA_LOVELACE_URL_PATH
