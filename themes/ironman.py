import svgwrite

def render(data):
    """
    Renders the Cinematic Iron Man theme.
    Logic: Deep 'Armor' background with glowing 'Repulsor' Yellow 
    and 'Arc' White high-intensity highlights.
    """
    contributions = data["contributions"][-365:] if len(data["contributions"]) > 365 else data["contributions"]

    cols = 53
    rows = 7
    width = cols * 15 + 20
    height = rows * 15 + 40

    dwg = svgwrite.Drawing(size=("100%", "100%"), viewBox=f"0 0 {width} {height}")
    
    # Deep 'Stealth Red' Background
    dwg.add(dwg.rect(insert=(0, 0), size=("100%", "100%"), fill="#1a0000"))

    box_size = 12
    gap = 3
    start_x = 10
    start_y = 10

    max_count = max((d["count"] for d in contributions), default=0)

    for i, day in enumerate(contributions):
        count = day["count"]
        col = i // rows
        row = i % rows
        x = start_x + col * (box_size + gap)
        y = start_y + row * (box_size + gap)

        if count == 0:
            fill_color = "#2d0000"  # Subtle armor plating
            stroke_color = "#3d0000"
            stroke_w = 0.5
        else:
            intensity = count / max_count if max_count > 0 else 0
            
            # Level 1: Muted Gold (Secondary plating)
            if intensity < 0.25:
                fill_color = "#c5a000"
                stroke_color = "#1a0000"
                stroke_w = 0.5
            # Level 2: Repulsor Yellow (Active power)
            elif intensity < 0.65:
                fill_color = "#ffcc00"
                stroke_color = "#ffffff"
                stroke_w = 0.3 # Slight glow hint
            # Level 3: Arc White (Full power)
            else:
                fill_color = "#ffffff"
                stroke_color = "#ffcc00"
                stroke_w = 1.0 # Strong energy border
            
        dwg.add(
            dwg.rect(
                insert=(x, y),
                size=(box_size, box_size),
                fill=fill_color,
                stroke=stroke_color,
                stroke_width=stroke_w,
                rx=2,
                ry=2,
            )
        )

    # Cinematic Legend
    legend_y = height - 14
    
    def legend_entry(x, label, color):
        dwg.add(dwg.rect(insert=(x, legend_y - 7), size=(9, 9), fill=color, rx=1))
        dwg.add(dwg.text(label, insert=(x + 13, legend_y + 1), 
                         fill="#ffffff", 
                         font_size=10, 
                         font_weight="bold",
                         letter_spacing="1px",
                         font_family="Orbitron, monospace"))

    legend_entry(10, "STBY", "#2d0000")
    legend_entry(65, "ARMOR", "#c5a000")
    legend_entry(135, "POWER", "#ffcc00")
    legend_entry(205, "ARC", "#ffffff")

    return dwg.tostring()