"""
Glass, Neural, and other advanced themed contribution visualizations.
"""
import math
from .themes_base import weeks_to_cells


def render_glass_theme(dwg, data, theme, weeks, cols, rows, max_date, width, height, animations_enabled=True, CSS_ANIMATIONS=""):
    """Render Glass theme: glassmorphic liquid interface."""
    # Theme Variables
    bg_col = theme.get("bg_color", "#050511")
    title_col = theme.get("title_color", "#00e5ff")
    text_col = theme.get("text_color", "#e0e0e0")
    border_col = theme.get("border_color", "white")

    # Basic stats to make the card feel more like a dashboard
    contributions = data.get("contributions", [])
    total_commits = data.get("total_commits", sum(d.get("count", 0) for d in contributions))
    active_days = sum(1 for d in contributions if d.get("count", 0) > 0)
    
    # --- 1. Defining Filters & Gradients ---
    
    # Blur filter for background blobs
    blob_blur = dwg.filter(id="blobBlur", x="-50%", y="-50%", width="200%", height="200%")
    blob_blur.feGaussianBlur(in_="SourceGraphic", stdDeviation=40)
    dwg.defs.add(blob_blur)
    
    # Glow filter for text
    text_glow = dwg.filter(id="textGlow")
    text_glow.feGaussianBlur(in_="SourceAlpha", stdDeviation=2, result="blur")
    text_glow.feOffset(in_="blur", dx=0, dy=0, result="offsetBlur")
    text_glow.feFlood(flood_color=title_col, result="glowColor")
    text_glow.feComposite(in_="glowColor", in2="offsetBlur", operator="in", result="coloredBlur")
    text_glow.feMerge(["coloredBlur", "SourceGraphic"])
    dwg.defs.add(text_glow)
    
    # Glass Panel Gradient
    glass_grad = dwg.linearGradient(start=(0, 0), end=(1, 1), id="glassGrad")
    glass_grad.add_stop_color(0, "white", opacity=0.15)
    glass_grad.add_stop_color(1, "white", opacity=0.05)
    dwg.defs.add(glass_grad)
    
    # Border Gradient
    border_grad = dwg.linearGradient(start=(0, 0), end=(1, 1), id="borderGrad")
    border_grad.add_stop_color(0, border_col, opacity=0.4)
    border_grad.add_stop_color(1, border_col, opacity=0.1)
    dwg.defs.add(border_grad)

    # Attach shared CSS animations for a more interactive feel
    if animations_enabled:
        dwg.defs.add(dwg.style(CSS_ANIMATIONS))

    # --- 2. Background Base ---
    dwg.add(dwg.rect(insert=(0, 0), size=("100%", "100%"), rx=16, ry=16, fill=bg_col))

    # --- 3. Neon Blobs (The "Liquid") ---
    dwg.add(dwg.circle(center=(0, 0), r=120, fill="#ff00ff", filter="url(#blobBlur)", opacity=0.6))
    dwg.add(dwg.circle(center=(width, height), r=140, fill="#00ffff", filter="url(#blobBlur)", opacity=0.5))
    dwg.add(dwg.circle(center=(width*0.8, height*0.3), r=80, fill=title_col, filter="url(#blobBlur)", opacity=0.6))
    dwg.add(dwg.circle(center=(width*0.2, height*1.1), r=100, fill="#2563eb", filter="url(#blobBlur)", opacity=0.6))

    # --- 4. The Glass Panel ---
    margin = 25
    panel_width = width - margin * 2
    panel_height = height - margin * 2
    
    dwg.add(dwg.rect(insert=(margin, margin), size=(panel_width, panel_height), rx=16, ry=16, fill="#000000", opacity=0.3))
    panel_rect = dwg.rect(
        insert=(margin, margin),
        size=(panel_width, panel_height),
        rx=16,
        ry=16,
        fill="url(#glassGrad)",
        stroke="url(#borderGrad)",
        stroke_width=1.2,
    )
    if animations_enabled:
        panel_rect["class"] = "anim-border-pulse"
    dwg.add(panel_rect)
    
    # More subtle Top Reflection
    reflection_grad = dwg.linearGradient(start=(0, 0), end=(0, 1), id="reflGrad")
    reflection_grad.add_stop_color(0, "white", opacity=0.08)
    reflection_grad.add_stop_color(1, "white", opacity=0)
    dwg.defs.add(reflection_grad)
    dwg.add(dwg.rect(insert=(margin + 4, margin + 4), size=(panel_width - 8, panel_height / 4), rx=12, ry=12, fill="url(#reflGrad)"))

    # --- 5. Content ---
    title = f"{data.get('username', 'Unknown')}'s Contributions"
    
    # More elegant typography
    base_title_size = 18
    name_len = len(title)
    
    # Scale font size more gracefully
    if name_len > 20:
        dynamic_font_size = max(11, base_title_size - (name_len - 20) // 1.5)
    else:
        dynamic_font_size = base_title_size

    # Use a more modern looking font stack and thinner weight for elegance
    title_text = dwg.text(
        title.upper(),
        insert=(width / 2, margin + 38),
        fill="white",
        font_size=dynamic_font_size,
        font_family="'Inter', system-ui, sans-serif",
        font_weight="800",
        text_anchor="middle",
        letter_spacing=2,
        filter="url(#textGlow)",
    )
    if animations_enabled:
        title_text["class"] = "anim-fade-in"
    dwg.add(title_text)
    
    subtitle = dwg.text(
        "GEOM-LIQUID INTERFACE",
        insert=(width / 2, margin + 55),
        fill=text_col,
        font_size=8,
        font_family="'Inter', sans-serif",
        letter_spacing=4,
        text_anchor="middle",
        opacity=0.6,
    )
    if animations_enabled:
        subtitle["class"] = "anim-slide-up"
    dwg.add(subtitle)

    # --- 6. Contributions Grid (Bubbles) - kept inside surrounding box ---
    contributions_subset = contributions[-119:]  # Fit 17 cols x 7 rows
    grid_cols = 17
    grid_rows = 7
    
    # Panel content area: below subtitle, with comfortable padding from panel edges
    grid_area_top = margin + 60
    grid_area_bottom = height - margin - 20
    grid_area_height = grid_area_bottom - grid_area_top
    # Size grid so 7 rows fit inside panel; circles stay in surrounding box
    step_y = grid_area_height / grid_rows
    step_x = (panel_width - 30) / (grid_cols - 1)  # 15px margin each side
    step_x = min(step_x, 26)
    cell_size = min(step_x, step_y) * 0.8
    radius = max(2, min(cell_size / 2, 5))
    # Center grid in panel
    grid_total_width = (grid_cols - 1) * step_x
    grid_total_height = (grid_rows - 1) * step_y
    start_x = margin + (panel_width - grid_total_width) / 2
    start_y = grid_area_top + (grid_area_height - grid_total_height) / 2
    
    # Clip path so contribution circles stay inside the glass panel
    clip_id = "glassPanelClip"
    clip = dwg.defs.add(dwg.clipPath(id=clip_id))
    clip.add(dwg.rect(insert=(margin, margin), size=(panel_width, panel_height), rx=16, ry=16))
    grid_group = dwg.g(clip_path=f"url(#{clip_id})")
    
    for i, day in enumerate(contributions_subset):
        col = i // grid_rows
        row = i % grid_rows
        
        cx = start_x + col * step_x
        cy = start_y + row * step_y
        
        count = day.get("count", 0)
        
        r = radius
        if count > 0:
            intensity = min(count / 10, 1)
            bubble = dwg.circle(
                center=(cx, cy),
                r=r,
                fill=title_col,
                opacity=0.4 + intensity * 0.5,
            )
            highlight = dwg.circle(
                center=(cx - r * 0.3, cy - r * 0.4),
                r=r * 0.4,
                fill="#ffffff",
                opacity=0.5,
            )

            if animations_enabled:
                classes = ["anim-bubble"]
                if intensity >= 0.7:
                    classes.append("anim-pulse-glow")
                delay = 0.02 * col + 0.01 * row
                bubble["class"] = " ".join(classes)
                bubble["style"] = f"animation-delay: {delay:.2f}s"
                highlight["class"] = " ".join(classes)
                highlight["style"] = f"animation-delay: {delay:.2f}s"

            grid_group.add(bubble)
            grid_group.add(highlight)
        else:
            bubble = dwg.circle(
                center=(cx, cy),
                r=r,
                fill="#ffffff",
                opacity=0.12,
            )
            if animations_enabled:
                delay = 0.02 * col + 0.01 * row
                bubble["class"] = "anim-bubble"
                bubble["style"] = f"animation-delay: {delay:.2f}s"
            grid_group.add(bubble)
    
    dwg.add(grid_group)


def render_neural_theme(dwg, data, theme, weeks, cols, rows, max_date, width, height):
    """Render Neural theme: brain network visualization."""
    cx = width / 2
    cy = height / 2 + 10

    contributions = data.get("contributions", [])[-80:]
    if not contributions:
        return dwg.tostring()

    nodes = []

    # --- Brain core glow ---
    dwg.add(dwg.circle(center=(cx, cy), r=45, fill="#00f7ff", opacity=0.08))
    dwg.add(dwg.text(
        "Contributions",
        insert=(cx, cy + 5),
        text_anchor="middle",
        fill="#00f7ff",
        font_size="12px",
        font_family="Courier New",
        opacity=0.8
    ))

    # --- Generate brain-shaped neuron positions ---
    for i, day in enumerate(contributions):
        count = day.get("count", 0)

        # Hemisphere split
        side = -1 if i % 2 == 0 else 1

        # Organic brain ellipse (deterministic)
        angle = (i / max(len(contributions), 1)) * math.pi
        radius_x = 90 + (i % 10) * 6
        radius_y = 60 + (i % 7) * 6

        # Distortion noise derived from count
        noise = 0.9 + ((count % 5) * 0.03)

        x = cx + side * math.cos(angle) * radius_x * noise
        y = cy + math.sin(angle) * radius_y * noise

        # Visual weight
        size = 2 + min(count, 10)
        brightness = min(255, 80 + count * 18)
        color = f"rgb(0,{brightness},255)"

        dwg.add(dwg.circle(
            center=(x, y),
            r=size,
            fill=color,
            opacity=0.9
        ))

        nodes.append((x, y, count))

    # --- Synapse connections ---
    for i in range(len(nodes)):
        x1, y1, c1 = nodes[i]

        for step in (1, 3, 7):
            j = i + step
            if j >= len(nodes):
                continue

            x2, y2, c2 = nodes[j]

            dist = math.hypot(x2 - x1, y2 - y1)

            if dist < 140:
                opacity = min((c1 + c2) / 20, 0.5)

                dwg.add(dwg.line(
                    start=(x1, y1),
                    end=(x2, y2),
                    stroke="#00f7ff",
                    stroke_width=1,
                    opacity=opacity
                ))


def render_default_theme(dwg, data, theme, weeks, cols, rows, max_date, width, height):
    """Render Default theme: classic GitHub-style grid."""
    from .themes_base import levels_from_cells, grid_positions, weeks_to_cells, add_timeline_labels
    
    # Just simple squares
    box_size = 7
    gap = 2
    start_x = 26
    start_y = 72
    cells = weeks_to_cells(weeks, cols, rows, max_date)
    max_count = max((cell["count"] for cell in cells if not cell["is_future"]), default=0)
    levels = levels_from_cells(cells, max_count)
    positions = grid_positions(cols, rows, start_x, start_y, box_size, gap)

    add_timeline_labels(dwg, weeks, cols, rows, start_x, start_y, box_size, gap, theme)

    colors = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]

    for idx, (x, y) in enumerate(positions):
        level = levels[idx]
        if level is None:
            continue
        fill = colors[level]
        dwg.add(dwg.rect(insert=(x, y), size=(box_size, box_size), fill=fill, rx=2, ry=2))
