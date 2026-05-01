import svgwrite

def render(data):
    """
    Renders the Spider-Man theme with balanced Red and Blue.
    Text is White for visibility.
    """
    contributions = data["contributions"][-365:] if len(data["contributions"]) > 365 else data["contributions"]

    cols = 53
    rows = 7
    width = cols * 15 + 20
    height = rows * 15 + 40

    dwg = svgwrite.Drawing(size=("100%", "100%"), viewBox=f"0 0 {width} {height}")
    
    # Solid Black Background
    dwg.add(dwg.rect(insert=(0, 0), size=("100%", "100%"), fill="#050505"))

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
            fill_color = "#121212" # Black/Grey
            stroke_color = "#222222"
        else:
            intensity = count / max_count if max_count > 0 else 0
            
            # Level 1: White (Highlight - minimal use)
            if intensity < 0.15:
                fill_color = "#ffffff" 
            # Level 2: Spider-Blue (Dominant mid-range)
            elif intensity < 0.55:
                fill_color = "#005aff"
            # Level 3: Spider-Red (Dominant peak)
            else:
                fill_color = "#ff0000"
            
            stroke_color = "#000000"

        dwg.add(
            dwg.rect(
                insert=(x, y),
                size=(box_size, box_size),
                fill=fill_color,
                stroke=stroke_color,
                stroke_width=0.8,
                rx=2,
                ry=2,
            )
        )

    # Legend - White Text for perfect visibility
    legend_y = height - 14
    legend_x = 10
    
    def legend_entry(x, label, color):
        dwg.add(dwg.rect(insert=(x, legend_y - 7), size=(9, 9), fill=color, rx=1))
        dwg.add(dwg.text(label, insert=(x + 13, legend_y + 1), 
                         fill="#ffffff", 
                         font_size=10, 
                         font_weight="bold",
                         font_family="Arial, sans-serif"))

    legend_entry(legend_x, "Noir", "#121212")
    legend_entry(legend_x + 55, "Web", "#ffffff")
    legend_entry(legend_x + 105, "Suit", "#005aff")
    legend_entry(legend_x + 160, "Hero", "#ff0000")

    return dwg.tostring()