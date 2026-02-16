#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
║                         ADARYUS R. GILLUM - CUSTOM NAME SNAKE GENERATOR                                                                              ║
║              Generates an animated SVG where a snake traces out "ADARYUS" letter by letter                                                           ║
╚══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
"""

import os
import svgwrite

# Letter definitions as coordinate paths (5x7 grid for each letter)
LETTERS = {
    'A': [
        (0, 6), (1, 3), (2, 0), (3, 3), (4, 6),  # Left diagonal and down
        (3, 3), (1, 3),  # Crossbar
    ],
    'D': [
        (0, 0), (0, 6),  # Vertical line
        (0, 0), (2, 0), (3, 1), (3, 5), (2, 6), (0, 6)  # Curve
    ],
    'R': [
        (0, 0), (0, 6),  # Vertical
        (0, 0), (2, 0), (3, 1), (3, 2), (2, 3), (0, 3),  # Top curve
        (1, 3), (3, 6)  # Leg
    ],
    'Y': [
        (0, 0), (2, 3), (4, 0),  # V shape
        (2, 3), (2, 6)  # Stem
    ],
    'U': [
        (0, 0), (0, 5), (1, 6), (3, 6), (4, 5), (4, 0)  # U curve
    ],
    'S': [
        (3, 0), (1, 0), (0, 1), (0, 2), (1, 3), (3, 3), (4, 4), (4, 5), (3, 6), (1, 6)  # S curve
    ]
}

def scale_points(points, offset_x, offset_y, scale=15):
    """Scale and offset points for positioning"""
    return [(x * scale + offset_x, y * scale + offset_y) for x, y in points]

def create_letter_snake():
    """Create an animated SVG with a snake that writes ADARYUS"""
    
    width = 800
    height = 220
    
    dwg = svgwrite.Drawing('dist/letter-snake.svg', size=(width, height), profile='full')
    
    # Definitions
    defs = dwg.defs
    
    # Gradient
    grad = dwg.linearGradient(id="snakeGrad", x1="0%", y1="0%", x2="100%", y2="0%")
    grad.add_stop_color(0, "#ff0000")
    grad.add_stop_color(0.25, "#ff6600")
    grad.add_stop_color(0.5, "#ffff00")
    grad.add_stop_color(0.75, "#00ff00")
    grad.add_stop_color(1, "#00ffff")
    defs.add(grad)
    
    # Glow filter
    glow = dwg.filter(id="glow", x="-50%", y="-50%", width="200%", height="200%")
    glow.add_gaussian_blur("3", result="blur")
    glow.feMerge(result="glow")
    glow.feMergeNode(in_="blur")
    glow.feMergeNode(in_="SourceGraphic")
    defs.add(glow)
    
    # Background
    dwg.add(dwg.rect(insert=(0, 0), size=(width, height), fill="#0d1117"))
    
    # Grid
    for x in range(0, width, 20):
        for y in range(0, height, 20):
            dwg.add(dwg.rect(insert=(x, y), size=(18, 18), fill="#161b22", rx=2))
    
    name = "ADARYUS"
    letter_spacing = 110
    base_x = 60
    base_y = 40
    
    # Generate paths for each letter
    for i, letter in enumerate(name):
        if letter in LETTERS:
            offset_x = base_x + (i * letter_spacing)
            points = scale_points(LETTERS[letter], offset_x, base_y)
            
            # Create path
            path_d = f"M {points[0][0]},{points[0][1]}"
            for p in points[1:]:
                path_d += f" L {p[0]},{p[1]}"
            
            path_length = len(points) * 20
            
            # Draw letter path
            path = dwg.path(
                d=path_d,
                fill="none",
                stroke="url(#snakeGrad)",
                stroke_width=5,
                stroke_linecap="round",
                stroke_linejoin="round",
                filter="url(#glow)"
            )
            
            # Staggered animation for each letter
            delay = i * 1.2
            path.add(dwg.animate(
                attributeName="stroke-dasharray",
                values=f"0,{path_length};{path_length},0",
                dur="8s",
                begin=f"{delay}s",
                repeatCount="indefinite"
            ))
            path.add(dwg.animate(
                attributeName="stroke-dashoffset",
                values=f"{path_length};0",
                dur="8s",
                begin=f"{delay}s",
                repeatCount="indefinite"
            ))
            
            dwg.add(path)
            
            # Snake head for this letter
            head = dwg.circle(center=points[0], r=7, fill="#ff0000", filter="url(#glow)")
            head_motion = dwg.animateMotion(
                dur="8s",
                repeatCount="indefinite",
                begin=f"{delay}s",
                path=path_d
            )
            head.add(head_motion)
            dwg.add(head)
            
            # Letter label
            label_x = offset_x + 30
            label = dwg.text(
                letter,
                insert=(label_x, 160),
                fill="#ff0000",
                font_family="monospace",
                font_size="18",
                font_weight="bold",
                text_anchor="middle"
            )
            label.add(dwg.animate(
                attributeName="opacity",
                values="0.2;1;0.2",
                dur="2s",
                begin=f"{delay}s",
                repeatCount="indefinite"
            ))
            dwg.add(label)
    
    # Title
    title = dwg.text(
        "ADARYUS R. GILLUM",
        insert=(width/2, 20),
        fill="#ff0000",
        font_family="monospace",
        font_size="16",
        font_weight="bold",
        text_anchor="middle"
    )
    title.add(dwg.animate(
        attributeName="opacity",
        values="0.5;1;0.5",
        dur="2s",
        repeatCount="indefinite"
    ))
    dwg.add(title)
    
    # Subtitle
    dwg.add(dwg.text(
        "The snake writes my name, one letter at a time",
        insert=(width/2, 200),
        fill="#00ff00",
        font_family="monospace",
        font_size="10",
        text_anchor="middle",
        opacity=0.7
    ))
    
    dwg.save()
    print("✅ Generated letter-snake.svg")

def create_dark_version():
    """Create a dark mode version of the SVG"""
    with open('dist/letter-snake.svg', 'r') as f:
        content = f.read()
    content = content.replace('#0d1117', '#000000').replace('#161b22', '#111111')
    with open('dist/letter-snake-dark.svg', 'w') as f:
        f.write(content)
    print("✅ Generated letter-snake-dark.svg")

if __name__ == "__main__":
    print("🐍 Generating ADARYUS letter-by-letter snake animation...")
    print("=" * 80)
    
    os.makedirs('dist', exist_ok=True)
    
    # Generate main SVG
    create_letter_snake()
    
    # Generate dark version
    create_dark_version()
    
    print("=" * 80)
    print("🎉 All snake files generated successfully!")
    print("\nFiles created:")
    print("  📄 dist/letter-snake.svg")
    print("  📄 dist/letter-snake-dark.svg")
