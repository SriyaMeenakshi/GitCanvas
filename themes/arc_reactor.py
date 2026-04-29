import svgwrite
import math
import random

def render(data):
    """
    Arc Reactor Theme - Advanced Version
    Mechanical + energy + electric feel
    """

    contributions = data['contributions'][-100:] if data.get('contributions') else []

    width = 800
    height = 400

    dwg = svgwrite.Drawing(size=("100%", "100%"), viewBox=f"0 0 {width} {height}")

    # Background
    dwg.add(dwg.rect(insert=(0, 0), size=("100%", "100%"), fill="#020617"))

    cx, cy = width / 2, height / 2

    # 🔵 Outer glow
    for r, opacity in [(140, 0.04), (120, 0.06), (100, 0.08)]:
        dwg.add(dwg.circle(center=(cx, cy), r=r, fill="#00eaff", opacity=opacity))

    # 🟤 Copper mechanical ring
    dwg.add(dwg.circle(
        center=(cx, cy),
        r=110,
        fill="none",
        stroke="#b87333",
        stroke_width=8,
        opacity=0.7
    ))

    # 🔷 Energy segments (reactor panels)
    segments = 12
    for i in range(segments):
        angle = (i / segments) * 2 * math.pi
        x1 = cx + math.cos(angle) * 85
        y1 = cy + math.sin(angle) * 85
        x2 = cx + math.cos(angle) * 105
        y2 = cy + math.sin(angle) * 105

        dwg.add(dwg.line(
            start=(x1, y1),
            end=(x2, y2),
            stroke="#00eaff",
            stroke_width=4,
            opacity=0.8
        ))

    # 🔵 Inner glow rings
    for r in [70, 50]:
        dwg.add(dwg.circle(center=(cx, cy), r=r, fill="none", stroke="#4cc9f0", stroke_width=2, opacity=0.5))

    # ⚪ Core (bright)
    dwg.add(dwg.circle(center=(cx, cy), r=25, fill="#e0f7ff", opacity=0.9))

    # 🔷 Inner energy core
    dwg.add(dwg.circle(center=(cx, cy), r=15, fill="#00eaff", opacity=1))

    if not contributions:
        return dwg.tostring()

    max_count = max(d['count'] for d in contributions) or 1

    # ⚡ Energy nodes (around reactor)
    for i, day in enumerate(contributions):
        count = day['count']

        angle = (i / len(contributions)) * 2 * math.pi
        distance = 130 + (count / max_count) * 60

        x = cx + math.cos(angle) * distance
        y = cy + math.sin(angle) * distance

        # color mapping
        if count == 0:
            color = "#1e293b"
        elif count < 3:
            color = "#4cc9f0"
        elif count < 6:
            color = "#00eaff"
        else:
            color = "#e0f7ff"

        dwg.add(dwg.circle(
            center=(x, y),
            r=2 + (count / max_count) * 3,
            fill=color,
            opacity=0.9
        ))

        # connection lines
        if count > 0:
            dwg.add(dwg.line(
                start=(cx, cy),
                end=(x, y),
                stroke="#00eaff",
                stroke_width=0.4,
                opacity=0.25
            ))

    # ⚡ Electric arcs (random lightning effect)
    random.seed(42)
    for _ in range(8):
        angle = random.uniform(0, 2 * math.pi)
        r1 = random.uniform(40, 80)
        r2 = r1 + random.uniform(10, 30)

        x1 = cx + math.cos(angle) * r1
        y1 = cy + math.sin(angle) * r1
        x2 = cx + math.cos(angle) * r2
        y2 = cy + math.sin(angle) * r2

        dwg.add(dwg.line(
            start=(x1, y1),
            end=(x2, y2),
            stroke="#e0f7ff",
            stroke_width=1,
            opacity=0.6
        ))

    # Title (minimal gold removed)
    dwg.add(dwg.text(
        "ARC REACTOR",
        insert=(cx, 40),
        text_anchor="middle",
        fill="#4cc9f0",
        font_size="20px",
        font_family="Segoe UI"
    ))

    return dwg.tostring()