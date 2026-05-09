from __future__ import annotations

import os
import shutil
from pathlib import Path

import pytest
from ha_testcontainer import HATestContainer, HAVersion

REPO_ROOT = Path(__file__).parent.parent
HA_CONFIG_DIR = REPO_ROOT / "tests" / "ha-config"
DIST_JS = REPO_ROOT / "dist" / "slider-entity-row.js"
HA_LOVELACE_URL_PATH = "lovelace"


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


@pytest.fixture(scope="session")
def ha_lovelace_url_path() -> str:
    return HA_LOVELACE_URL_PATH
