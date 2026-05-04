"""
Gaming and arcade-style contribution themes.
"""
from .themes_base import levels_from_cells, grid_positions, weeks_to_cells, add_timeline_labels


def render_gaming_theme(dwg, data, theme, weeks, cols, rows, max_date, width, height):
    """Render Gaming theme: Snake-like contribution grid."""
    grid_size = 7
    gap = 2
    start_x = 26
    start_y = 72
    cells = weeks_to_cells(weeks, cols, rows, max_date)
    max_count = max((cell["count"] for cell in cells if not cell["is_future"]), default=0)
    levels = levels_from_cells(cells, max_count)
    positions = grid_positions(cols, rows, start_x, start_y, grid_size, gap)

    add_timeline_labels(dwg, weeks, cols, rows, start_x, start_y, grid_size, gap, theme)
    
    # Draw a simple grid path (Snake body) taking up space
    dwg.add(dwg.text(f"SCORE: {data.get('total_commits', '0')}", insert=(width-120, 30),
                     fill=theme["text_color"], font_family="Courier New", font_size=16, font_weight="bold"))
    
    # Draw grid cells based on real contribution levels
    colors = [theme["bg_color"], "#0e4429", "#006d32", "#26a641", "#39d353"]
    last_active_index = None

    for idx, (x, y) in enumerate(positions):
        level = levels[idx]
        if level is None:
            continue
        fill = colors[level]
        dwg.add(dwg.rect(insert=(x, y), size=(grid_size, grid_size), fill=fill, rx=2, ry=2))
        if level > 0:
            last_active_index = idx

        # Apples represent peak contribution days
        if level == 4:
            dwg.add(dwg.rect(insert=(x, y), size=(grid_size, grid_size), fill="#FF3333", rx=2, ry=2))

    # Snake head at last active cell
    if last_active_index is not None:
        hx, hy = positions[last_active_index]
        dwg.add(dwg.rect(insert=(hx, hy), size=(grid_size, grid_size), fill=theme["title_color"], rx=2, ry=2))
        dwg.add(dwg.rect(insert=(hx + 1, hy + 2), size=(2, 2), fill="black"))
        dwg.add(dwg.rect(insert=(hx + 4, hy + 2), size=(2, 2), fill="black"))


def render_pacman_theme(dwg, data, theme, weeks, cols, rows, max_date, width, height):
    """Render Pac-Man arcade theme with contribution pellets."""
    # Maze grid lines
    for i in range(0, width, 25):
        dwg.add(dwg.line(start=(i, 50), end=(i, height-10), stroke="#1919a6", stroke_width=0.5, opacity=0.3))
    
    # Get actual contribution data
    box_size = 7
    gap = 2
    start_x = 26
    start_y = 72
    
    cells = weeks_to_cells(weeks, cols, rows, max_date)
    max_count = max((cell["count"] for cell in cells if not cell["is_future"]), default=0)
    levels = levels_from_cells(cells, max_count)
    positions = grid_positions(cols, rows, start_x, start_y, box_size, gap)
    
    add_timeline_labels(dwg, weeks, cols, rows, start_x, start_y, box_size, gap, theme)
    
    # Draw pellets based on actual contribution levels
    for idx, (x, y) in enumerate(positions):
        level = levels[idx]
        if level is None:
            continue
        
        center_x = x + box_size // 2
        center_y = y + box_size // 2
        
        if level == 0:
            # Empty space - small dot
            dwg.add(dwg.circle(center=(center_x, center_y), r=1.5, fill="#333333"))
        elif level >= 4:
            # Power pellet (high activity)
            dwg.add(dwg.circle(center=(center_x, center_y), r=4, fill="#ffb8ae"))
            # Pulsing effect
            dwg.add(dwg.circle(center=(center_x, center_y), r=5, fill="none", 
                             stroke="#ffb8ae", stroke_width=1, opacity=0.5))
        else:
            # Regular pellet - color based on level
            colors = ["#4169e1", "#ff8c00", "#ffff00"]  # Blue, Orange, Yellow
            dwg.add(dwg.circle(center=(center_x, center_y), r=3, fill=colors[level-1]))
    
    # Pac-Man character
    pacman_x = 15
    pacman_y = 75
    pacman_path = dwg.path(d=f"M {pacman_x} {pacman_y} " +
                          f"L {pacman_x + 10} {pacman_y - 8} " +
                          f"A 10 10 0 1 1 {pacman_x + 10} {pacman_y + 8} Z",
                          fill="#ffff00")
    dwg.add(pacman_path)
    
    # Score display using actual commits
    dwg.add(dwg.text(f"SCORE: {data.get('total_commits', '0')}", 
                    insert=(width-120, 35), 
                    fill="#ffff00", 
                    font_family="Courier New", 
                    font_size=12, 
                    font_weight="bold"))
