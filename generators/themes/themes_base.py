"""
Shared utilities for contribution card theme rendering.

This module contains helper functions used across all themes.
"""
import math
from datetime import date, datetime, timedelta, timezone


def levels_from_cells(cells, max_count):
    """Convert contribution cell counts to intensity levels (0-4)."""
    levels = []
    for cell in cells:
        if cell.get("is_future"):
            levels.append(None)
            continue
        count = cell.get("count", 0)
        if count <= 0 or max_count == 0:
            levels.append(0)
            continue
        ratio = count / max_count
        if ratio <= 0.25:
            levels.append(1)
        elif ratio <= 0.5:
            levels.append(2)
        elif ratio <= 0.75:
            levels.append(3)
        else:
            levels.append(4)
    return levels


def grid_positions(cols, rows, start_x, start_y, box_size, gap):
    """Calculate grid positions for contribution cells."""
    positions = []
    for col in range(cols):
        for row in range(rows):
            x = start_x + col * (box_size + gap)
            y = start_y + row * (box_size + gap)
            positions.append((x, y))
    return positions


def weeks_to_cells(weeks, cols, rows, max_date):
    """Convert weeks data to cells with metadata."""
    cells = []
    for col in range(cols):
        week = weeks[col] if col < len(weeks) else []
        for row in range(rows):
            day = week[row] if row < len(week) else {"date": None, "count": 0}
            item_date = day.get("date") if day else None
            parsed = None
            if item_date:
                try:
                    parsed = date.fromisoformat(item_date)
                except (TypeError, ValueError):
                    parsed = None
            is_future = bool(max_date and parsed and parsed > max_date)
            cells.append({
                "date": item_date,
                "count": day.get("count", 0),
                "is_future": is_future
            })
    return cells


def add_timeline_labels(dwg, weeks, cols, rows, start_x, start_y, box_size, gap, theme):
    """Add month and day labels to contribution grid."""
    last_month = None
    max_label_x = start_x + (cols - 1) * (box_size + gap)

    for col, week in enumerate(weeks):
        day = week[0] if week else None
        day_date = None
        if day and day.get("date"):
            try:
                day_date = date.fromisoformat(day["date"])
            except (TypeError, ValueError):
                day_date = None

        if not day_date:
            continue

        month_label = day_date.strftime("%b")
        if month_label != last_month:
            x = start_x + col * (box_size + gap) - 2
            if x > max_label_x - 10:
                x = max_label_x - 10
            y = start_y - 10
            dwg.add(dwg.text(
                month_label,
                insert=(x, y),
                fill=theme["text_color"],
                font_size=9,
                font_family=theme["font_family"],
                opacity=0.8
            ))
            last_month = month_label

    label_x = start_x - 24
    label_rows = {1: "Mon", 3: "Wed", 5: "Fri"}
    for row, label in label_rows.items():
        y = start_y + row * (box_size + gap) + box_size - 1
        dwg.add(dwg.text(
            label,
            insert=(label_x, y),
            fill=theme["text_color"],
            font_size=9,
            font_family=theme["font_family"],
            opacity=0.8
        ))
