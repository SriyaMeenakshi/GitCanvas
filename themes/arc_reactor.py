import svgwrite

def render(data):
    """
    Renders the Arc Reactor Energy Wave.
    Logic: Cyan frequency bars representing energy output levels.
    """

    contributions = data['contributions'][-100:] if data.get('contributions') else []

    width = 800
    height = 400

    dwg = svgwrite.Drawing(size=("100%", "100%"), viewBox=f"0 0 {width} {height}")

    # Background: Deep Stark-Tech Black
    dwg.add(dwg.rect(insert=(0, 0), size=("100%", "100%"), fill="#010409"))

    # HUD Title
    dwg.add(dwg.text(
        "CORE ENERGY MONITOR",
        insert=(width / 2, 40),
        text_anchor="middle",
        fill="#ffffff",
        font_size="22px",
        font_family="Orbitron, Segoe UI, sans-serif",
        font_weight="bold"
    ))

    if not contributions:
        return dwg.tostring()

    num_bars = len(contributions)
    bar_width = max(1, (width - 40) / num_bars - 2)
    center_y = height / 2
    max_amp = height / 2 - 40
    max_commits = max(d['count'] for d in contributions) or 1
    start_x = 20

    # HUD Corner Accents (Technical symbols)
    dwg.add(dwg.text("⟁", insert=(15, 35), fill="#00eaff", font_size="18px"))
    dwg.add(dwg.text("⟁", insert=(width - 35, 35), fill="#00eaff", font_size="18px"))

    for i, day in enumerate(contributions):
        count = day['count']
        normalized = count / max_commits
        amp = normalized * max_amp + 3
        x = start_x + i * (bar_width + 2)

        # ⚡ Color Logic: Shifting from Dark Cyan to Glowing White
        if count == 0:
            color = "#002b2b"  # Standby
        elif count < 3:
            color = "#008b8b"  # Low Power (Dark Cyan)
        elif count < 6:
            color = "#00eaff"  # Active (Electric Cyan)
        else:
            color = "#ffffff"  # Overdrive (Core White)

        # Energy Bar (Waveform style)
        dwg.add(dwg.rect(
            insert=(x, center_y - amp),
            size=(bar_width, amp * 2),
            fill=color,
            rx=1,
            ry=1
        ))

        # Add "Pulse" glow for peak activity
        if count >= max_commits and count > 5:
             dwg.add(dwg.circle(
                center=(x + bar_width/2, center_y - amp - 8),
                r=2,
                fill="#ffffff",
                opacity=0.8
            ))

    # Static baseline (HUD Detail)
    dwg.add(dwg.line(
        start=(20, center_y), 
        end=(width-20, center_y), 
        stroke="#00eaff", 
        stroke_width=0.5, 
        opacity=0.3
    ))

    return dwg.tostring()