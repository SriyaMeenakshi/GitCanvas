import svgwrite
from themes.styles import THEMES


def _mood_visuals(mood):
    mood_map = {
        "Shipping": ("#3fb950", "ROCKET ON"),
        "Bug Hunting": ("#f85149", "BUG HUNT"),
        "Refactoring": ("#58a6ff", "CLEANUP MODE"),
        "Maintenance": ("#d29922", "MAINTENANCE"),
        "General Coding": ("#a371f7", "FLOW STATE"),
        "No Signal": ("#8b949e", "NO DATA"),
    }
    return mood_map.get(mood, ("#8b949e", "FLOW STATE"))


def draw_commit_analysis_card(data, theme_name="Default", custom_colors=None):
    """
    Generate SVG card for commit-message analysis.

    Expected data keys:
    - username
    - total_messages
    - average_length
    - mood
    - mood_score
    - common_words (list of {word, count})
    """
    theme = THEMES.get(theme_name, THEMES["Default"]).copy()
    if custom_colors:
        theme.update(custom_colors)

    words = data.get("common_words", [])[:10]
    total_messages = data.get("total_messages", 0)
    average_length = data.get("average_length", 0.0)
    mood = data.get("mood", "No Signal")
    mood_score = data.get("mood_score", 0.0)
    username = data.get("username", "Unknown")

    width = 500
    height = 250
    dwg = svgwrite.Drawing(size=("100%", "100%"), viewBox=f"0 0 {width} {height}")

    dwg.add(dwg.rect(
        insert=(0, 0),
        size=("100%", "100%"),
        rx=10,
        ry=10,
        fill=theme["bg_color"],
        stroke=theme["border_color"],
        stroke_width=2,
    ))

    dwg.add(dwg.text(
        "Commit Message Analysis",
        insert=(20, 30),
        fill=theme["title_color"],
        font_size=18,
        font_family=theme.get("font_family", "Arial"),
        font_weight="bold",
    ))

    dwg.add(dwg.text(
        f"@{username}",
        insert=(20, 47),
        fill=theme["text_color"],
        font_size=11,
        font_family=theme.get("font_family", "Arial"),
        opacity=0.75,
    ))

    stat_y = 72
    stat_gap = 20
    stats = [
        ("Messages Scanned", f"{total_messages}"),
        ("Avg Length", f"{average_length} chars"),
    ]

    for idx, (label, value) in enumerate(stats):
        y = stat_y + (idx * stat_gap)
        dwg.add(dwg.text(
            label,
            insert=(20, y),
            fill=theme["text_color"],
            font_size=11,
            font_family=theme.get("font_family", "Arial"),
            opacity=0.85,
        ))
        dwg.add(dwg.text(
            value,
            insert=(170, y),
            fill=theme["title_color"],
            font_size=11,
            font_family=theme.get("font_family", "Arial"),
            font_weight="bold",
        ))

    mood_color, mood_label = _mood_visuals(mood)
    mood_box_y = 112
    dwg.add(dwg.rect(
        insert=(20, mood_box_y),
        size=(210, 60),
        rx=8,
        ry=8,
        fill="none",
        stroke=mood_color,
        stroke_width=1.5,
        opacity=0.9,
    ))

    dwg.add(dwg.text(
        "Coding Mood",
        insert=(32, mood_box_y + 20),
        fill=theme["text_color"],
        font_size=10,
        font_family=theme.get("font_family", "Arial"),
        opacity=0.8,
    ))

    dwg.add(dwg.text(
        mood_label,
        insert=(32, mood_box_y + 40),
        fill=mood_color,
        font_size=16,
        font_family=theme.get("font_family", "Arial"),
        font_weight="bold",
    ))

    dwg.add(dwg.text(
        f"Confidence: {mood_score}%",
        insert=(32, mood_box_y + 54),
        fill=theme["text_color"],
        font_size=9,
        font_family=theme.get("font_family", "Arial"),
        opacity=0.7,
    ))

    # Word cloud area
    cloud_x = 260
    cloud_y = 64
    cloud_w = 220
    cloud_h = 165
    dwg.add(dwg.rect(
        insert=(cloud_x, cloud_y),
        size=(cloud_w, cloud_h),
        rx=8,
        ry=8,
        fill="none",
        stroke=theme["border_color"],
        stroke_width=1,
        opacity=0.5,
    ))
    dwg.add(dwg.text(
        "Top Words",
        insert=(cloud_x + 12, cloud_y + 18),
        fill=theme["text_color"],
        font_size=10,
        font_family=theme.get("font_family", "Arial"),
        opacity=0.8,
    ))

    if not words:
        dwg.add(dwg.text(
            "No commit text available",
            insert=(cloud_x + 12, cloud_y + 40),
            fill=theme["text_color"],
            font_size=11,
            font_family=theme.get("font_family", "Arial"),
            opacity=0.7,
        ))
    else:
        max_count = max((item.get("count", 1) for item in words), default=1)
        row = 0
        col = 0
        for item in words:
            word = item.get("word", "")
            count = item.get("count", 1)
            if not word:
                continue

            # Scale font between 10-20 based on term frequency.
            size = 10 + int((count / max_count) * 10) if max_count else 10
            x = cloud_x + 12 + (col * 70)
            y = cloud_y + 38 + (row * 28)
            dwg.add(dwg.text(
                word,
                insert=(x, y),
                fill=theme["title_color"] if (row + col) % 2 == 0 else theme["text_color"],
                font_size=size,
                font_family=theme.get("font_family", "Arial"),
                font_weight="bold" if size >= 16 else "normal",
                opacity=0.95,
            ))

            col += 1
            if col >= 3:
                col = 0
                row += 1
            if y > cloud_y + cloud_h - 8:
                break

    return dwg.tostring()
