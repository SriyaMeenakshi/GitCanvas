"""
Neon and cyberpunk-themed contribution visualizations.
"""
from .themes_base import levels_from_cells, grid_positions, weeks_to_cells, add_timeline_labels


def render_cyberpunk_theme(dwg, data, theme, weeks, cols, rows, max_date, width, height):
    """Render Cyberpunk theme: neon grid with high-tech aesthetic."""
    # Neon grid background
    for i in range(0, width, 20):
        dwg.add(dwg.line(start=(i, 0), end=(i, height), stroke="#1a1a2e", stroke_width=0.3, opacity=0.5))
    for i in range(0, height, 20):
        dwg.add(dwg.line(start=(0, i), end=(width, i), stroke="#1a1a2e", stroke_width=0.3, opacity=0.5))
    
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
    
    # Neon blocks based on actual contribution levels
    neon_colors = ["#1a1a2e", "#00ffff", "#00ff41", "#ff00ff", "#ff0080"]
    
    for idx, (x, y) in enumerate(positions):
        level = levels[idx]
        if level is None:
            continue
        
        fill_color = neon_colors[level]
        
        if level == 0:
            dwg.add(dwg.rect(insert=(x, y), size=(box_size, box_size), fill=fill_color, rx=1, opacity=0.5))
        else:
            dwg.add(dwg.rect(insert=(x, y), size=(box_size, box_size), fill=fill_color, rx=1, opacity=0.7))
            
            if level >= 3:  # Glow effect for high activity
                dwg.add(dwg.rect(insert=(x-1, y-1), size=(box_size+2, box_size+2), 
                               fill="none", stroke=fill_color, stroke_width=1, rx=2, opacity=0.3))
    
    # Scan line effect
    scan_y = 90
    dwg.add(dwg.line(start=(0, scan_y), end=(width, scan_y), stroke="#00ff41", stroke_width=1.5, opacity=0.2))


def render_ocean_theme(dwg, data, theme, weeks, cols, rows, max_date, width, height):
    """Render Ocean theme: underwater with fish representing contributions."""
    # Background waves at top
    wave_path = "M0,45 Q60,35 120,45 T240,45 T360,45 T480,45 T500,45 L500,0 L0,0 Z"
    dwg.add(dwg.path(d=wave_path, fill=theme.get("border_color", "#004466"), opacity=0.5))
    
    # Coral reefs at bottom
    coral_y = height - 25
    dwg.add(dwg.path(d=f"M50,{coral_y} Q70,{coral_y-15} 90,{coral_y} Q110,{coral_y-12} 130,{coral_y} Z", 
                    fill="#8B4513", opacity=0.6))
    dwg.add(dwg.path(d=f"M200,{coral_y} Q220,{coral_y-18} 240,{coral_y} Q260,{coral_y-14} 280,{coral_y} Z", 
                    fill="#A0522D", opacity=0.6))
    dwg.add(dwg.path(d=f"M350,{coral_y} Q370,{coral_y-16} 390,{coral_y} Q410,{coral_y-13} 430,{coral_y} Z", 
                    fill="#8B4513", opacity=0.6))
    
    # Bubbles floating up
    for i in range(8):
        bubble_x = 40 + i * 60
        bubble_y = 55 + (i % 3) * 12
        dwg.add(dwg.circle(center=(bubble_x, bubble_y), r=2, fill="#66ddaa", opacity=0.4))
        dwg.add(dwg.circle(center=(bubble_x, bubble_y), r=3, fill="none", stroke="#66ddaa", 
                         stroke_width=0.5, opacity=0.3))
    
    # Contribution grid as fish
    box_size = 6
    gap = 3
    start_x = 26
    start_y = 70
    cells = weeks_to_cells(weeks, cols, rows, max_date)
    max_count = max((cell["count"] for cell in cells if not cell["is_future"]), default=0)
    positions = grid_positions(cols, rows, start_x, start_y, box_size, gap)
    
    # Add timeline labels
    add_timeline_labels(dwg, weeks, cols, rows, start_x, start_y, box_size, gap, theme)
    
    # Draw fish based on contribution intensity
    for idx, (x, y) in enumerate(positions):
        cell = cells[idx] if idx < len(cells) else None
        if not cell or cell.get("is_future"):
            continue

        count = cell.get("count", 0)
        if count <= 0:
            # Empty cell - small bubble
            dwg.add(dwg.circle(center=(x + 3, y + 3), r=1.4, 
                             fill=theme.get("text_color", "#66ddaa"), opacity=0.5))
            continue

        # Fish size based on contribution intensity
        intensity = 0 if max_count == 0 else count / max_count
        fish_w = 8 + int(6 * intensity)
        fish_h = 4 + int(4 * intensity)
        
        # Fish colors based on intensity
        if intensity < 0.25:
            fish_color = "#5599cc"
        elif intensity < 0.5:
            fish_color = "#4488bb"
        elif intensity < 0.75:
            fish_color = "#2277aa"
        else:
            fish_color = "#0066aa"

        # Fish body (triangle)
        body = f"M{x},{y} L{x + fish_w},{y - fish_h} L{x + fish_w},{y + fish_h} Z"
        dwg.add(dwg.path(d=body, fill=fish_color, opacity=0.9))
        
        # Add fin for high activity fish
        if intensity > 0.6:
            fin = f"M{x + fish_w // 2},{y} L{x + fish_w - 2},{y - 3} L{x + fish_w - 2},{y + 3} Z"
            dwg.add(dwg.path(d=fin, fill=fish_color, opacity=0.9))
            
            # Eye dot for biggest fish
            if intensity > 0.8:
                dwg.add(dwg.circle(center=(x + fish_w - 3, y), r=0.7, fill="#ffffff", opacity=0.8))
