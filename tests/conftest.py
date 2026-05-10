from __future__ import annotations

import os
from functools import partial
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

os.environ.setdefault("HA_CONFIG_PATH", str(REPO_ROOT / "tests" / "ha-config"))
os.environ.setdefault("HA_PLUGINS_YAML", str(REPO_ROOT / "tests" / "plugins.yaml"))

import ha_testcontainer.visual.scenario_runner as _sr  # noqa: E402

_sr.SCENARIOS_DIR = REPO_ROOT / "tests" / "visual" / "scenarios"
_sr.SNAPSHOTS_DIR = REPO_ROOT / "tests" / "visual" / "snapshots"
_sr.REPO_ROOT = REPO_ROOT
_sr.DOCS_SCENARIOS_DIR = _sr.REPO_ROOT / "docs" / "scenarios"
_TRUTHY_ENV_VALUES = {"1", "true", "yes", "on"}

# Keep backward compatibility with existing local scripts/docs that still set
# VISUAL_UPDATE, while ha-testcontainer snapshot assertions use SNAPSHOT_UPDATE.
if os.environ.get("VISUAL_UPDATE", "").strip().lower() in _TRUTHY_ENV_VALUES:
    os.environ.setdefault("SNAPSHOT_UPDATE", "1")

# Ensure snapshot assertions always read/write baselines in this repository.
# conftest is imported before tests are collected, so this override is active for test runs.
_sr.assert_snapshot = partial(_sr.assert_snapshot, snapshots_dir=_sr.SNAPSHOTS_DIR)
