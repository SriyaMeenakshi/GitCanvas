import svgwrite
import math
import random

def render(data):
    """
    Cybersecurity Theme - Hacker Terminal Style
    Contributions are code breaches on the network
    High activity = system compromised
    """
    contributions = data['contributions'][-365:] if len(data['contributions']) > 365 else data['contributions']

    cols = 53
    rows = 7
    width = cols * 15 + 120
    height = rows * 15 + 160

    dwg = svgwrite.Drawing(size=("100%", "100%"), viewBox=f"0 0 {width} {height}")

    # Dark background
    dwg.add(dwg.rect(insert=(0, 0), size=("100%", "100%"), fill="#0d0d0d"))

    # Title
    dwg.add(dwg.text("🔐 CYBERSECURITY", insert=(width//2, 30),
        text_anchor="middle", font_size="18px",
        font_family="Courier New", fill="#00ff41", font_weight="bold"))

    dwg.add(dwg.text("> scanning contributions...", insert=(width//2, 48),
        text_anchor="middle", font_size="10px",
        font_family="Courier New", fill="#00aa2a"))

    # Contribution cells
    cell_size = 11
    padding_x = 60
    padding_y = 60

    max_contrib = max(contributions) if contributions else 1

    for i, count in enumerate(contributions):
        col = i // rows
        row = i % rows
        x = padding_x + col * 13
        y = padding_y + row * 13

        if count == 0:
            color = "#0d1f0d"
        elif count < max_contrib * 0.25:
            color = "#003300"
        elif count < max_contrib * 0.5:
            color = "#006600"
        elif count < max_contrib * 0.75:
            color = "#00cc00"
        else:
            color = "#00ff41"

        dwg.add(dwg.rect(insert=(x, y), size=(cell_size, cell_size),
            fill=color, rx=2, ry=2))

    # Footer
    dwg.add(dwg.text("[ACCESS GRANTED] Keep committing! 💻", insert=(width//2, height-15),
        text_anchor="middle", font_size="10px",
        font_family="Courier New", fill="#00ff41"))

    return dwg.tostring()