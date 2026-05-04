"""
Sports and athletic-themed contribution visualizations.
"""
from .themes_base import levels_from_cells, grid_positions, weeks_to_cells, add_timeline_labels


def render_cricket_theme(dwg, data, theme, weeks, cols, rows, max_date, width, height):
    """Render Cricket theme: stadium with contribution runs."""
    # Stadium lights
    for i in range(3):
        light_x = 80 + i * 150
        light_y = 45
        dwg.add(dwg.circle(center=(light_x, light_y), r=4, fill="#ffeb3b", opacity=0.8))
        dwg.add(dwg.circle(center=(light_x, light_y), r=7, fill="#ffeb3b", opacity=0.3))
    
    # Cricket field boundary
    field_center_x = width // 2
    field_center_y = height // 2 + 20
    dwg.add(dwg.ellipse(center=(field_center_x, field_center_y), r=(200, 50), 
                       fill="none", stroke="#ffffff", stroke_width=2, 
                       stroke_dasharray="5,5", opacity=0.4))
    
    # Contribution boxes as runs - using ACTUAL GitHub data
    box_size = 7
    gap = 2
    start_x = 26
    start_y = 72
    
    # Get actual contribution data
    cells = weeks_to_cells(weeks, cols, rows, max_date)
    max_count = max((cell["count"] for cell in cells if not cell["is_future"]), default=0)
    levels = levels_from_cells(cells, max_count)
    positions = grid_positions(cols, rows, start_x, start_y, box_size, gap)
    
    # Add timeline labels
    add_timeline_labels(dwg, weeks, cols, rows, start_x, start_y, box_size, gap, theme)
    
    # Draw contribution grid with cricket scoring
    for idx, (x, y) in enumerate(positions):
        level = levels[idx]
        if level is None:
            continue
            
        if level == 0:
            # Duck (out) - no contributions
            dwg.add(dwg.rect(insert=(x, y), size=(box_size, box_size), 
                           fill="#8b4513", rx=1, opacity=0.3))
        else:
            # Runs: 1, 2, 4, 6 based on contribution levels
            colors = ["#90ee90", "#7fbf7f", "#ffd700", "#ff6b35"]
            scores = ["1", "2", "4", "6"]
            fill_color = colors[min(level-1, 3)]
            score = scores[min(level-1, 3)]
            
            dwg.add(dwg.rect(insert=(x, y), size=(box_size, box_size), 
                           fill=fill_color, rx=1, opacity=0.8))
            
            # Score number
            dwg.add(dwg.text(score, insert=(x + box_size//2, y + box_size//2 + 2), 
                           font_size="6px", fill="#000000", text_anchor="middle", 
                           font_weight="bold", opacity=0.6))
            
            # Glow for sixes (highest contribution level)
            if level == 4:
                dwg.add(dwg.rect(insert=(x-1, y-1), size=(box_size+2, box_size+2), 
                               fill="none", stroke="#ff6b35", stroke_width=1, 
                               rx=2, opacity=0.5))
    
    # Cricket bat
    bat_x = width - 60
    bat_y = height - 50
    dwg.add(dwg.rect(insert=(bat_x, bat_y - 25), size=(4, 25), fill="#8b4513", rx=1))
    dwg.add(dwg.rect(insert=(bat_x - 6, bat_y), size=(16, 35), fill="#d2691e", rx=2))
    
    # Cricket ball
    ball_x = bat_x + 30
    ball_y = bat_y + 15
    dwg.add(dwg.circle(center=(ball_x, ball_y), r=5, fill="#cc0000"))
    
    # Wickets
    wicket_x = 25
    wicket_y = height - 40
    for i in range(3):
        dwg.add(dwg.rect(insert=(wicket_x + i * 4, wicket_y), size=(2, 25), fill="#f5deb3"))
    dwg.add(dwg.rect(insert=(wicket_x - 1, wicket_y - 2), size=(11, 2), fill="#8b4513", rx=1))
    
    # Scoreboard will show actual total commits
    total_commits = data.get('total_commits', 0)
    dwg.add(dwg.text(f"RUNS: {total_commits}", insert=(width - 110, 30), 
                    font_size="12px", font_family="monospace", fill="#00ff00", 
                    font_weight="bold"))
