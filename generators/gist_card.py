import svgwrite
from themes.styles import THEMES


def draw_gist_card(data, theme_name="Default", custom_colors=None, style_variant="code", show_description=True):
    """
    Generate a stylized gist embed card SVG.

    data keys:
    - description
    - html_url
    - updated_at
    - filename
    - language
    - size
    - preview
    """
    theme = THEMES.get(theme_name, THEMES["Default"]).copy()
    if custom_colors:
        theme.update(custom_colors)

    description = data.get("description") or "Untitled Gist"
    filename = data.get("filename") or "unknown.txt"
    language = data.get("language") or "Text"
    size = data.get("size") or 0
    updated_at = data.get("updated_at") or ""
    preview = data.get("preview") or ""

    if style_variant == "compact":
        width = 500
        height = 170
        max_preview_lines = 4
        preview_font_size = 10
    else:
        width = 500
        height = 230
        max_preview_lines = 8
        preview_font_size = 10

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
        "Gist Embed",
        insert=(20, 30),
        fill=theme["title_color"],
        font_size=18,
        font_family=theme.get("font_family", "Arial"),
        font_weight="bold",
    ))

    if show_description:
        desc_text = description[:64] + "..." if len(description) > 64 else description
        dwg.add(dwg.text(
            desc_text,
            insert=(20, 48),
            fill=theme["text_color"],
            font_size=11,
            font_family=theme.get("font_family", "Arial"),
            opacity=0.85,
        ))

    meta_y = 70 if show_description else 48
    dwg.add(dwg.text(
        filename,
        insert=(20, meta_y),
        fill=theme["title_color"],
        font_size=12,
        font_family=theme.get("font_family", "Arial"),
        font_weight="bold",
    ))

    dwg.add(dwg.text(
        f"{language} | {size} bytes",
        insert=(20, meta_y + 16),
        fill=theme["text_color"],
        font_size=10,
        font_family=theme.get("font_family", "Arial"),
        opacity=0.75,
    ))

    if updated_at:
        dwg.add(dwg.text(
            f"Updated: {updated_at[:10]}",
            insert=(width - 20, meta_y + 16),
            fill=theme["text_color"],
            font_size=9,
            font_family=theme.get("font_family", "Arial"),
            text_anchor="end",
            opacity=0.7,
        ))

    # Code preview block
    preview_top = meta_y + 28
    preview_height = height - preview_top - 18
    dwg.add(dwg.rect(
        insert=(20, preview_top),
        size=(width - 40, preview_height),
        rx=8,
        ry=8,
        fill="#0f1720",
        stroke=theme["border_color"],
        stroke_width=1,
        opacity=0.95,
    ))

    lines = preview.splitlines()[:max_preview_lines]
    if not lines:
        lines = ["No preview content available"]

    y = preview_top + 18
    for line in lines:
        truncated = line[:72] + "..." if len(line) > 72 else line
        dwg.add(dwg.text(
            truncated.replace("\t", "    "),
            insert=(30, y),
            fill="#c9d1d9",
            font_size=preview_font_size,
            font_family="Courier New, monospace",
        ))
        y += 16

    return dwg.tostring()
