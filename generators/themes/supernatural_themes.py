"""
Supernatural and dark-themed contribution visualizations.
"""
import math
import random
from .themes_base import levels_from_cells, grid_positions, weeks_to_cells, add_timeline_labels


def render_stranger_things_theme(dwg, data, theme, weeks, cols, rows, max_date, width, height):
    """Render Stranger Things theme: Upside Down with demogorgon."""
    # Floating particles
    random.seed(42)
    for i in range(15):
        x = random.randint(20, width-20)
        y = random.randint(40, height-20)
        r = random.randint(1, 2)
        dwg.add(dwg.circle(center=(x, y), r=r, fill="#ffffff", opacity=0.3))
    
    # Contribution grid with red glow using ACTUAL GitHub data
    box_size = 7
    gap = 2
    start_x = 26
    start_y = 72
    
    cells = weeks_to_cells(weeks, cols, rows, max_date)
    max_count = max((cell["count"] for cell in cells if not cell["is_future"]), default=0)
    levels = levels_from_cells(cells, max_count)
    positions = grid_positions(cols, rows, start_x, start_y, box_size, gap)

    add_timeline_labels(dwg, weeks, cols, rows, start_x, start_y, box_size, gap, theme)
    
    # Red-tinted colors for Stranger Things theme
    colors = ["#1a1a1a", "#8b0000", "#b22222", "#dc143c", "#ff0000"]
    
    for idx, (x, y) in enumerate(positions):
        level = levels[idx]
        if level is None:
            continue
        fill = colors[level]
        
        dwg.add(dwg.rect(insert=(x, y), size=(box_size, box_size), fill=fill, rx=1, opacity=0.7))
        
        if level == 4:  # High activity - add glow
            dwg.add(dwg.rect(insert=(x-1, y-1), size=(box_size+2, box_size+2), 
                           fill="none", stroke="#ff0000", stroke_width=0.5, opacity=0.4))
    
    # Mini demogorgon silhouette
    demo_x = width - 50
    demo_y = height - 50
    dwg.add(dwg.circle(center=(demo_x, demo_y), r=15, fill="#330000", opacity=0.6))
    
    # Petals
    for angle in range(0, 360, 60):
        rad = math.radians(angle)
        x1 = demo_x + 12 * math.cos(rad)
        y1 = demo_y + 12 * math.sin(rad)
        x2 = demo_x + 20 * math.cos(rad)
        y2 = demo_y + 20 * math.sin(rad)
        dwg.add(dwg.line(start=(x1, y1), end=(x2, y2), stroke="#ff0000", stroke_width=1.5, opacity=0.5))
