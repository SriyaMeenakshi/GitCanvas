"""
Contribution card SVG generator with support for multiple visual themes.

This module provides a central entry point for generating contribution cards
with different visual themes. Theme-specific rendering logic is delegated to
dedicated functions in the themes module.
"""
import logging
import svgwrite
from datetime import date, datetime, timedelta, timezone
from themes.styles import THEMES
from .svg_base import CSS_ANIMATIONS
from .themes import THEME_DISPATCHER, render_default_theme

logger = logging.getLogger(__name__)


def _latest_contribution_date(contributions):
    max_date = None
    for item in contributions:
        item_date = item.get("date") if item else None
        if not item_date:
            continue
        try:
            parsed = date.fromisoformat(item_date)
        except (TypeError, ValueError):
            continue
        if not max_date or parsed > max_date:
            max_date = parsed

    today = datetime.now(timezone.utc).date()
    if max_date and max_date > today:
        return today
    return max_date


def _weeks_from_dates(contributions, cols, rows):
    if not contributions:
        return [[{"date": None, "count": 0} for _ in range(rows)] for _ in range(cols)], None

    date_counts = {}
    for item in contributions:
        item_date = item.get("date")
        # Explicit type checking and validation
        if not isinstance(item_date, str) or not item_date.strip():
            continue
        try:
            parsed = date.fromisoformat(item_date)
        except ValueError:
            logger.warning(f"Invalid date format: {item_date}")
            continue
        date_counts[parsed] = item.get("count", 0)

    max_date = _latest_contribution_date(contributions)
    if not max_date:
        return [[{"date": None, "count": 0} for _ in range(rows)] for _ in range(cols)], None

    days_to_sunday = (max_date.weekday() + 1) % 7
    end_week_start = max_date - timedelta(days=days_to_sunday)
    start_week_start = end_week_start - timedelta(days=(cols - 1) * 7)

    weeks = []
    for col in range(cols):
        week_start = start_week_start + timedelta(days=col * 7)
        week = []
        for row in range(rows):
            day_date = week_start + timedelta(days=row)
            week.append({
                "date": day_date.isoformat(),
                "count": date_counts.get(day_date, 0)
            })
        weeks.append(week)

    return weeks, max_date


def _resolve_weeks(contributions, contribution_weeks, cols, rows):
    """Resolve contribution weeks, preferring provided data over computed."""
    if contribution_weeks:
        weeks = contribution_weeks[-cols:]
        normalized = []
        for week in weeks:
            week_days = list(week) if week else []
            if len(week_days) < rows:
                week_days = week_days + ([{"date": None, "count": 0}] * (rows - len(week_days)))
            normalized.append(week_days[:rows])
        if len(normalized) < cols:
            pad = [[{"date": None, "count": 0} for _ in range(rows)] for _ in range(cols - len(normalized))]
            normalized = pad + normalized
        return normalized, _latest_contribution_date(contributions)

    return _weeks_from_dates(contributions, cols, rows)


def draw_contrib_card(data, theme_name="Default", custom_colors=None, date_range=None, animations_enabled=True):
    """
    Generates a Contribution Graph Card SVG with theme-specific visualization.
    
    Supports multiple themes including Gaming, Space, Marvel, Stranger_things,
    Pacman, Cyberpunk, Cricket, Ocean, Glass, Neural, Matrix, and Default.
    
    Args:
        data: Dict containing contribution data with 'contributions' list
        theme_name: String name of the theme to use (case-sensitive)
        custom_colors: Optional dict of custom color overrides
        date_range: Optional dict with 'start' and 'end' date strings (YYYY-MM-DD)
                    to filter contributions. If None, shows all contributions.
        animations_enabled: Whether to enable CSS animations (default: True)
    
    Returns:
        SVG string for the contribution card
    """
    # Save original theme name for comparison
    original_theme_name = theme_name
    
    # Get theme configuration
    theme = THEMES.get(theme_name, THEMES["Default"]).copy()
    if custom_colors:
        theme.update(custom_colors)
    
    # Determine canvas size based on theme
    width = 500
    height = 170
    
    # Allow larger canvas for Gaming theme
    if original_theme_name == "Gaming":
        width = 560
        height = 180
    
    # Create SVG drawing
    dwg = svgwrite.Drawing(size=("100%", "100%"), viewBox=f"0 0 {width} {height}")
    
    # Add background
    dwg.add(dwg.rect(insert=(0, 0), size=("100%", "100%"), rx=10, ry=10, 
                     fill=theme["bg_color"], stroke=theme["border_color"], stroke_width=2))
    
    # Add title
    username = data.get('username', 'Unknown')
    title = f"{username}'s Contributions"
    dwg.add(dwg.text(title, insert=(20, 24), 
                     fill=theme["title_color"], 
                     font_size=theme.get("title_font_size", 18), 
                     font_family=theme.get("font_family", "Arial"), 
                     font_weight="bold"))
    
    # Prepare contribution data
    contributions = data.get("contributions", [])
    
    # Filter contributions by date range if provided
    if date_range:
        from utils.github_api import filter_contributions_by_date
        contributions = filter_contributions_by_date(contributions, date_range)
    
    # Calculate grid dimensions
    total_days = len(contributions)
    cols = 53 if total_days >= 371 else 52
    rows = 7
    
    # Convert contributions to weekly grid
    weeks, max_date = _resolve_weeks(contributions, data.get("contribution_weeks"), cols, rows)
    
    # Handle special case: Matrix theme delegates to its own module
    if original_theme_name == "Matrix":
        from themes import matrix
        svg = matrix.render(data, theme)
        return svg
    
    # Get the appropriate theme renderer from dispatcher
    theme_renderer = THEME_DISPATCHER.get(original_theme_name)
    
    # If theme not in dispatcher, use default
    if theme_renderer is None:
        theme_renderer = render_default_theme
    
    # Call the theme-specific renderer
    theme_renderer(
        dwg, data, theme, weeks, cols, rows, max_date, 
        width, height
    )
    
    # For Glass theme, pass additional parameters
    if original_theme_name == "Glass":
        # Re-render Glass theme with animation support
        from .themes.advanced_themes import render_glass_theme
        # Clear the SVG except for background and title (already added above)
        dwg = svgwrite.Drawing(size=("100%", "100%"), viewBox=f"0 0 {width} {height}")
        dwg.add(dwg.rect(insert=(0, 0), size=("100%", "100%"), rx=10, ry=10, 
                         fill=theme["bg_color"], stroke=theme["border_color"], stroke_width=2))
        dwg.add(dwg.text(title, insert=(20, 24), 
                         fill=theme["title_color"], 
                         font_size=theme.get("title_font_size", 18), 
                         font_family=theme.get("font_family", "Arial"), 
                         font_weight="bold"))
        
        render_glass_theme(dwg, data, theme, weeks, cols, rows, max_date, width, height, animations_enabled, CSS_ANIMATIONS)
    
    return dwg.tostring()

