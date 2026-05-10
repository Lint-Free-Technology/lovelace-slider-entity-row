from __future__ import annotations

import pytest
from playwright.sync_api import Page

from ha_testcontainer.visual.scenario_runner import (
    clear_scenario,
    goto_scenario,
    load_all_scenarios,
    push_scenario,
    reset_theme,
    run_assertions,
    run_interactions,
    set_theme,
)

_ALL_SCENARIOS = load_all_scenarios()
_SCENARIO_IDS = [s["id"] for s in _ALL_SCENARIOS]
_SCENARIO_MAP = {s["id"]: s for s in _ALL_SCENARIOS}


def _assert_slider_rows_have_sliders(page: Page) -> None:
    """Validate slider rows render in the expected HA row/slider structure.

    Checks that the current scenario view contains `hui-generic-entity-row` rows.
    For every entities card that renders more than one generic row, verifies each
    row includes an `ha-slider`.
    """
    dom_summary = page.evaluate(
        """
        () => {
          const collectAll = (selector) => {
            const out = new Set();
            const visit = (root) => {
              if (!root || !root.querySelectorAll) {
                return;
              }
              for (const el of root.querySelectorAll(selector)) {
                out.add(el);
              }
              const children = root.children ? Array.from(root.children) : [];
              for (const child of children) {
                if (child.shadowRoot) {
                  visit(child.shadowRoot);
                }
                visit(child);
              }
            };
            visit(document);
            return Array.from(out);
          };

          const hasDeep = (root, selector) => {
            if (!root || !root.querySelectorAll) {
              return false;
            }
            if (root.querySelector(selector)) {
              return true;
            }
            const children = root.children ? Array.from(root.children) : [];
            for (const child of children) {
              if (child.shadowRoot && hasDeep(child.shadowRoot, selector)) {
                return true;
              }
              if (hasDeep(child, selector)) {
                return true;
              }
            }
            return false;
          };

          const genericRows = collectAll('hui-generic-entity-row');
          const entitiesCards = collectAll('hui-entities-card');
          let multiRowCards = 0;
          let rowsChecked = 0;
          let rowsMissingSlider = 0;

          for (const card of entitiesCards) {
            const rows = Array.from(card.querySelectorAll('hui-generic-entity-row'));
            if (rows.length > 1) {
              multiRowCards += 1;
              for (const row of rows) {
                rowsChecked += 1;
                if (!hasDeep(row, 'ha-slider') && !hasDeep(row.shadowRoot, 'ha-slider')) {
                  rowsMissingSlider += 1;
                }
              }
            }
          }

          return {
            genericRows: genericRows.length,
            multiRowCards,
            rowsChecked,
            rowsMissingSlider,
          };
        }
        """
    )

    assert dom_summary["genericRows"] > 0, "Expected rendered hui-generic-entity-row elements"
    assert dom_summary["multiRowCards"] > 0, "Expected at least one entities card with multiple generic rows"
    assert dom_summary["rowsChecked"] > 0, "Expected to check at least one generic row for slider rendering"
    assert dom_summary["rowsMissingSlider"] == 0, (
        "Expected each checked hui-generic-entity-row to contain ha-slider"
    )


@pytest.mark.parametrize("scenario_id", _SCENARIO_IDS)
def test_scenario(
    scenario_id: str,
    ha,
    ha_page: Page,
    ha_url: str,
    ha_lovelace_url_path: str,
) -> None:
    scenario = _SCENARIO_MAP[scenario_id]
    theme = scenario.get("theme")

    push_scenario(ha, ha_lovelace_url_path, scenario)
    if theme:
        set_theme(ha, theme)

    try:
        run_interactions(ha_page, scenario, ha=ha, key="setup")
        goto_scenario(ha_page, ha_url, ha_lovelace_url_path, scenario["view_path"])
        run_interactions(ha_page, scenario, ha=ha)
        if scenario_id != "04_errors":
            _assert_slider_rows_have_sliders(ha_page)
        run_assertions(ha_page, scenario)
    finally:
        run_interactions(ha_page, scenario, ha=ha, key="teardown")
        if theme:
            reset_theme(ha)
        clear_scenario(ha, ha_lovelace_url_path)
