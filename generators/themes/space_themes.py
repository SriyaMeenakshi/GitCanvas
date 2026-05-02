"""
Space and cosmic-themed contribution visualizations.
"""
from .themes_base import levels_from_cells, grid_positions, weeks_to_cells, add_timeline_labels


def render_space_theme(dwg, data, theme, weeks, cols, rows, max_date, width, height):
    """Render Space theme: starfield with spaceship."""
    dwg.defs.add(dwg.style("""
        @keyframes twinkle {
        0%   { opacity: 0.3; }
        50%  { opacity: 1; }
        100% { opacity: 0.3; }
        }

        .star {
        animation: twinkle 2s ease-in-out infinite;
        }
        """))

    cells = weeks_to_cells(weeks, cols, rows, max_date)
    max_count = max((cell["count"] for cell in cells if not cell["is_future"]), default=0)
    levels = levels_from_cells(cells, max_count)
    start_x = 26
    start_y = 72
    grid_size = 7
    gap = 2
    positions = grid_positions(cols, rows, start_x, start_y, grid_size, gap)

    add_timeline_labels(dwg, weeks, cols, rows, start_x, start_y, grid_size, gap, theme)

    for idx, (sx, sy) in enumerate(positions):
        level = levels[idx]
        if level is None:
            continue
        if level == 0:
            continue
        r = 1 + (level * 0.7)
        delay = (idx % 10) * 0.2

        star = dwg.circle(
            center=(sx + 5, sy + 5),
            r=r,
            fill="white",
            class_="star",
            style=f"animation-delay: {delay}s"
        )

        dwg.add(star)

    # Draw Spaceship (Simple triangle)
    ship_x = width - 60
    ship_y = height / 2 + 10
    
    # Flame
    dwg.add(dwg.path(d=f"M {ship_x-10} {ship_y} L {ship_x-20} {ship_y-5} L {ship_x-20} {ship_y+5} Z", fill="orange"))
    # Body
    dwg.add(dwg.path(d=f"M {ship_x} {ship_y} L {ship_x-15} {ship_y-8} L {ship_x-15} {ship_y+8} Z", fill="#00a8ff"))
    
    # Beam eating a star?
    dwg.add(dwg.line(start=(ship_x, ship_y), end=(width, ship_y), stroke="#00a8ff", stroke_width=2, stroke_dasharray="4,2"))


def render_marvel_theme(dwg, data, theme, weeks, cols, rows, max_date, width, height):
    """Render Marvel theme: Infinity Stones with contribution intensity glow."""
    box_size = 7
    gap = 2
    start_x = 26
    start_y = 72
    
    # Get actual contribution data
    cells = weeks_to_cells(weeks, cols, rows, max_date)
    max_count = max((cell["count"] for cell in cells if not cell["is_future"]), default=0)
    levels = levels_from_cells(cells, max_count)
    positions = grid_positions(cols, rows, start_x, start_y, box_size, gap)
    
    add_timeline_labels(dwg, weeks, cols, rows, start_x, start_y, box_size, gap, theme)
    
    # Infinity Stone colors (cycle through them for visual variety)
    stone_colors = [
        "#FFD700",  # Mind Stone (Yellow)
        "#FF0000",  # Reality Stone (Red)
        "#0099FF",  # Space Stone (Blue)
        "#9D00FF",  # Power Stone (Purple)
        "#00FF88",  # Time Stone (Green)
        "#FF6B35"   # Soul Stone (Orange)
    ]
    
    # Draw contribution grid as Infinity Stones
    for idx, (x, y) in enumerate(positions):
        level = levels[idx]
        if level is None:
            continue
        
        # Cycle through stone colors based on column for cleaner pattern
        col = idx // 7  # rows = 7
        stone_color = stone_colors[col % len(stone_colors)]
        center_x = x + box_size // 2
        center_y = y + box_size // 2
        
        if level == 0:
            # No contributions - very subtle stone
            dwg.add(dwg.circle(center=(center_x, center_y), r=2, 
                             fill=stone_color, opacity=0.1))
        else:
            # Contributions present - glowing stone based on intensity
            # More refined glow scaling
            glow_radius = 2.5 + (level * 1.2)
            stone_radius = 2 + (level * 0.6)
            glow_opacity = 0.15 + (level * 0.12)
            stone_opacity = 0.65 + (level * 0.08)
            
            # Outer glow
            dwg.add(dwg.circle(center=(center_x, center_y), r=glow_radius, 
                             fill=stone_color, opacity=glow_opacity))
            
            # Inner stone with subtle border
            dwg.add(dwg.circle(center=(center_x, center_y), r=stone_radius, 
                             fill=stone_color, opacity=stone_opacity, 
                             stroke="white", stroke_width=0.2))
            
            # Extra glow for highest activity (level 4) - more subtle
            if level == 4:
                dwg.add(dwg.circle(center=(center_x, center_y), r=glow_radius + 1.5, 
                                 fill=stone_color, opacity=0.1))
    
    # Subtle legend at bottom
    legend_y = height - 15
    legend_start_x = 30
    
    dwg.add(dwg.text("Less", insert=(legend_start_x, legend_y), 
                    fill=theme["text_color"], font_size=9, 
                    font_family=theme["font_family"], opacity=0.6))
    
    # Legend stones
    for i in range(5):
        lx = legend_start_x + 30 + (i * 12)
        level_opacity = 0.1 + (i * 0.2)
        level_size = 2 + (i * 0.5)
        dwg.add(dwg.circle(center=(lx, legend_y - 3), r=level_size, 
                         fill=stone_colors[0], opacity=level_opacity))
    
    dwg.add(dwg.text("More", insert=(legend_start_x + 90, legend_y), 
                    fill=theme["text_color"], font_size=9, 
                    font_family=theme["font_family"], opacity=0.6))
