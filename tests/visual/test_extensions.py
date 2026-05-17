from __future__ import annotations

from typing import TYPE_CHECKING, Any

from ha_testcontainer.visual.scenario_runner import register_assertion_type

if TYPE_CHECKING:
    from playwright.sync_api import Page

# ---------------------------------------------------------------------------
# Handler implementations
# ---------------------------------------------------------------------------

_CONTENT_WAIT_TIMEOUT = 20_000

def _wait_for_slider_scenario_content(page: Page) -> None:
    """Wait until rendered Lovelace content includes entities cards and slider rows.

    Raises Playwright TimeoutError if the scenario content does not appear
    within the configured wait timeout.
    """
    page.wait_for_function(
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
            return out.size;
          };

          return collectAll('hui-entities-card') > 0 && collectAll('slider-entity-row') > 0;
        }
        """,
        # Rendering can be slower on CI when HA initializes resources and custom cards.
        timeout=_CONTENT_WAIT_TIMEOUT,
    )


def assert_slider_rows_have_sliders(page: Page, assertion) -> None:
    """Validate slider rows render in the expected HA row/slider structure.

    Checks that the current scenario view contains `hui-generic-entity-row` rows.
    For each entities card that renders more than one generic row, performs
    deep shadow-DOM counting of row and `ha-slider` elements and fails if any
    such row is missing a slider.
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
          const sliderRows = collectAll('slider-entity-row');
          const countDeep = (root, selector) => {
            if (!root || !root.querySelectorAll) {
              return 0;
            }
            let count = root.querySelectorAll(selector).length;
            const children = root.children ? Array.from(root.children) : [];
            for (const child of children) {
              if (child.shadowRoot) {
                count += countDeep(child.shadowRoot, selector);
              }
              count += countDeep(child, selector);
            }
            return count;
          };

          let rowsChecked = 0;
          let rowsMissingSlider = 0;

          for (const card of entitiesCards) {
            if (!card.shadowRoot) {
              return {
                genericRows: genericRows.length,
                rowsChecked: 0,
                rowsMissingSlider: 0,
                error: 'Missing shadowRoot on hui-entities-card',
              };
            }
            const rows = countDeep(card.shadowRoot, 'hui-generic-entity-row');
            if (rows >= 1) {
              rowsChecked += rows;
              const sliders = countDeep(card.shadowRoot, 'ha-slider');
              rowsMissingSlider += Math.max(0, rows - sliders);
            }
          }

          return {
            genericRows: genericRows.length,
            entitiesCards: entitiesCards.length,
            sliderRows: sliderRows.length,
            rowsChecked,
            rowsMissingSlider,
          };
        }
        """
    )

    error = dom_summary.get("error")
    assert error is None, error
    assert dom_summary["entitiesCards"] > 0, "Expected rendered hui-entities-card elements"
    assert dom_summary["sliderRows"] > 0, "Expected rendered slider-entity-row elements"
    assert dom_summary["genericRows"] > 0, "Expected rendered hui-generic-entity-row elements"
    assert dom_summary["rowsChecked"] > 0, "Expected to check at least one generic row for slider rendering"
    assert dom_summary["rowsMissingSlider"] == 0, (
        "Expected each checked hui-generic-entity-row to contain ha-slider"
    )

register_assertion_type("slider_rows_have_sliders", assert_slider_rows_have_sliders)