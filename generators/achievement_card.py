import svgwrite
from themes.styles import THEMES
from .svg_base import create_svg_base
from utils.achievements import calculate_achievements

def draw_achievement_card(data, theme_name="Default", custom_colors=None, animations_enabled=True):
    """
    Generates a 'Trophy Room' SVG showing unlocked achievement badges.
    """
    achievements = calculate_achievements(data)
    unlocked = [a for a in achievements if a["unlocked"]]
    
    # If none unlocked, show a few locked ones as goals
    display_achievements = unlocked if unlocked else achievements[:3]
    
    # Use 2 items per row for professional spacing with long descriptions
    width = 600
    rows = (len(display_achievements) + 1) // 2
    height = 110 + (rows * 170)
    
    username = data.get('username', 'Unknown')
    dwg, theme = create_svg_base(theme_name, custom_colors, width, height, f"🏆 {username}'s Trophy Room", animations_enabled=animations_enabled)
    
    font_family = theme["font_family"]
    text_color = theme["text_color"]
    title_color = theme["title_color"]
    icon_color = theme["icon_color"]
    bg_color = theme["bg_color"]
    
    # Stats summary
    dwg.add(dwg.text(f"Achievements Unlocked: {len(unlocked)}/{len(achievements)}", 
                     insert=(20, 60), fill=text_color, font_size=13, 
                     font_family=font_family, opacity=0.8))

    # Grid positioning (2 columns)
    start_x = 50
    start_y = 95
    padding_x = 280
    padding_y = 170
    
    for i, ach in enumerate(display_achievements):
        col = i % 2
        row = i // 2
        
        x = start_x + (col * padding_x)
        y = start_y + (row * padding_y)
        
        # Badge Container
        is_locked = not ach["unlocked"]
        opacity = 1.0 if not is_locked else 0.4
        
        # Badge Base (Centered in column)
        center_x = x + 105
        
        # Glow effect for unlocked
        if not is_locked and animations_enabled:
            glow_color = "#FFD700" if ach["level"] == "Gold" else "#C0C0C0" if ach["level"] == "Silver" else "#CD7F32"
            dwg.add(dwg.circle(center=(center_x, y + 55), r=45, fill=glow_color, opacity=0.15, class_="anim-pulse-glow"))

        # Background hex or circle
        dwg.add(dwg.circle(center=(center_x, y + 55), r=48, fill=text_color, opacity=0.05))
        dwg.add(dwg.circle(center=(center_x, y + 55), r=48, fill="none", stroke=text_color, stroke_width=1.5, opacity=0.2))
        
        # Icon
        dwg.add(dwg.text(ach["icon"], insert=(center_x, y + 72), fill=icon_color, font_size=52, 
                         text_anchor="middle", font_family="Apple Color Emoji, Segoe UI Emoji, Noto Color Emoji"))
        
        # Level Badge
        if not is_locked:
            level_color = "#FFD700" if ach["level"] == "Gold" else "#C0C0C0" if ach["level"] == "Silver" else "#CD7F32"
            dwg.add(dwg.rect(insert=(center_x - 28, y + 92), size=(56, 22), rx=11, fill=level_color))
            dwg.add(dwg.text(ach["level"], insert=(center_x, y + 107), fill="#000", font_size=11, 
                             font_family=font_family, text_anchor="middle", font_weight="bold"))

        # Name
        dwg.add(dwg.text(ach["name"], insert=(center_x, y + 132), fill=title_color, font_size=16, 
                         font_family=font_family, text_anchor="middle", font_weight="bold"))
        
        # Description
        desc = ach["description"]
        dwg.add(dwg.text(desc, insert=(center_x, y + 154), fill=text_color, font_size=12, 
                         font_family=font_family, text_anchor="middle", opacity=0.9))

        if is_locked:
            # Lock overlay
            dwg.add(dwg.text("🔒", insert=(center_x, y + 65), fill=text_color, font_size=24, 
                             text_anchor="middle", opacity=0.5))

    return dwg.tostring()
