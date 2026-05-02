# generators/visual_elements.py

def emoji_element(emoji: str, size: int = 48) -> str:
    """
    Generate SVG for an emoji
    """
    return f"""
    <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}">
        <text x="50%" y="50%" dominant-baseline="middle"
              text-anchor="middle" font-size="{size}px">
            {emoji}
        </text>
    </svg>
    """


def gif_element(gif_url: str, size: int = 120) -> str:
    """
    Generate SVG wrapper for a GIF
    """
    return f"""
    <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}">
        <image href="{gif_url}" width="{size}" height="{size}" />
    </svg>
    """


def sticker_element(image_url: str, size: int = 100) -> str:
    """
    Generate SVG for a sticker / icon
    """
    return f"""
    <svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}">
        <image href="{image_url}" width="{size}" height="{size}" />
    </svg>
    """


def create_composite_canvas(svg_elements: list, bg_color: str = "#0d1117", padding: int = 20) -> str:
    """
    Combine multiple SVG elements into a single composite canvas.
    
    Args:
        svg_elements: List of SVG string elements
        bg_color: Background color hex code
        padding: Padding around elements
    
    Returns:
        A single composite SVG string containing all elements arranged in a grid
    """
    if not svg_elements:
        # Return empty canvas
        return f"""
        <svg xmlns="http://www.w3.org/2000/svg" width="600" height="400" viewBox="0 0 600 400">
            <rect width="600" height="400" fill="{bg_color}"/>
            <text x="300" y="200" text-anchor="middle" dominant-baseline="middle" 
                  fill="#888" font-size="16px" font-family="Arial">
                Your canvas is empty. Add elements to get started!
            </text>
        </svg>
        """
    
    # Calculate grid layout
    import math
    cols = math.ceil(math.sqrt(len(svg_elements)))
    rows = math.ceil(len(svg_elements) / cols)
    
    # Element dimensions
    element_width = 140
    element_height = 140
    
    # Canvas dimensions
    canvas_width = cols * (element_width + padding) + padding
    canvas_height = rows * (element_height + padding) + padding
    
    # Extract SVG content from each element (between <svg> tags)
    svg_content_list = []
    for idx, svg_str in enumerate(svg_elements):
        # Parse the SVG to extract its contents
        # Find content between opening and closing svg tags
        start = svg_str.find('>') + 1
        end = svg_str.rfind('</svg>')
        if start > 0 and end > start:
            content = svg_str[start:end]
            svg_content_list.append((idx, content))
    
    # Build composite SVG with grid layout
    composite = f"""
    <svg xmlns="http://www.w3.org/2000/svg" width="{canvas_width}" height="{canvas_height}" viewBox="0 0 {canvas_width} {canvas_height}">
        <rect width="{canvas_width}" height="{canvas_height}" fill="{bg_color}"/>
        <style>
            .canvas-border {{ stroke: #30363d; stroke-width: 1; fill: none; }}
        </style>
    """
    
    # Place elements in grid
    for idx, content in svg_content_list:
        col = idx % cols
        row = idx // cols
        x = padding + col * (element_width + padding)
        y = padding + row * (element_height + padding)
        
        composite += f"""
        <g transform="translate({x}, {y})">
            <rect x="0" y="0" width="{element_width}" height="{element_height}" 
                  class="canvas-border" rx="8"/>
            <g transform="translate({element_width/2}, {element_height/2}) scale(1)">
                {content}
            </g>
        </g>
        """
    
    composite += "</svg>"
    
    return composite
