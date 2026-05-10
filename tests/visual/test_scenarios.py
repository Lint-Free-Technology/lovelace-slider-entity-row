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
          const sliderRows = collectAll('slider-entity-row');
          let sliderRowsWithoutSlider = 0;

          for (const row of sliderRows) {
            if (!hasDeep(row.shadowRoot, 'ha-slider')) {
              sliderRowsWithoutSlider += 1;
            }
          }

          return {
            genericRows: genericRows.length,
            sliderRows: sliderRows.length,
            sliderRowsWithoutSlider,
          };
        }
        """
    )

    assert dom_summary["genericRows"] > 0, "Expected rendered hui-generic-entity-row elements"
    assert dom_summary["sliderRows"] > 0, "Expected rendered slider-entity-row elements"
    assert dom_summary["sliderRowsWithoutSlider"] == 0, (
        "Expected every rendered slider-entity-row element to contain ha-slider"
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
        if scenario_id == "03_width":
            _assert_slider_rows_have_sliders(ha_page)
        run_assertions(ha_page, scenario)
    finally:
        run_interactions(ha_page, scenario, ha=ha, key="teardown")
        if theme:
            reset_theme(ha)
        clear_scenario(ha, ha_lovelace_url_path)
