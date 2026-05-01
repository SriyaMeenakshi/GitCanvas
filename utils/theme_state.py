"""Helpers for Streamlit theme customization state."""

from __future__ import annotations

from typing import Any, MutableMapping


THEME_FILTER_KEYS = ("bg_color", "title_color", "text_color", "border_color")


def theme_filter_widget_keys(theme_name: str) -> dict[str, str]:
    """Return the Streamlit widget keys for the theme color controls."""
    return {
        "bg_color": f"customize_bg_{theme_name}",
        "title_color": f"customize_title_{theme_name}",
        "text_color": f"customize_text_{theme_name}",
        "border_color": f"customize_border_{theme_name}",
    }


def reset_theme_filter_state(
    session_state: MutableMapping[str, Any],
    theme_name: str,
    theme_defaults: MutableMapping[str, Any],
) -> None:
    """Reset theme color widgets to the defaults for the selected theme."""
    for color_key, widget_key in theme_filter_widget_keys(theme_name).items():
        session_state[widget_key] = theme_defaults.get(color_key, "#000000")