from __future__ import annotations

from typing import Any

SETUP_POST_NAVIGATION_INTERACTIONS = {
    "hover",
    "hover_away",
    "click",
    "dispatch_window_event",
}


def split_setup_interactions(
    scenario: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    setup = scenario.get("setup", [])
    setup_before_navigation = []
    setup_after_navigation = []

    for interaction in setup:
        if interaction.get("type") in SETUP_POST_NAVIGATION_INTERACTIONS:
            setup_after_navigation.append(interaction)
        else:
            setup_before_navigation.append(interaction)

    return setup_before_navigation, setup_after_navigation
