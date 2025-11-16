"""
Interactive Tangram Rotation & Position Debug Tool
Use keyboard to adjust rotation offset and position offset for each piece
"""

import pygame
import sys
import json

# Swan shape data
SWAN_PIECES = [
    {"color": "red", "center": [305, 290], "angle": 225, "piece_type": "large_triangle"},
    {"color": "green", "center": [401, 320], "angle": 135, "piece_type": "medium_triangle"},
    {"color": "blue", "center": [346, 335], "angle": 180, "piece_type": "large_triangle"},
    {"color": "yellow", "center": [426, 280], "angle": 315, "piece_type": "small_triangle"},
    {"color": "purple", "center": [418, 165], "angle": 270, "piece_type": "small_triangle"},
    {"color": "teal", "center": [399, 241], "angle": 315, "piece_type": "square"},
    {"color": "orange", "center": [378, 186], "angle": 315, "piece_type": "parallelogram"}
]

# Color mapping
COLORS = {
    'red': (255, 0, 0),
    'blue': (0, 0, 255),
    'yellow': (255, 255, 0),
    'green': (0, 255, 0),
    'orange': (255, 165, 0),
    'purple': (255, 0, 255),
    'teal': (0, 255, 255)
}

# Initialize Pygame
pygame.init()
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rotation Debug Tool - Press SPACE to cycle modes")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 24)
font_small = pygame.font.Font(None, 18)

# Global adjustment values
rotation_offset = 0  # Add this to all angles
x_offset = 0
y_offset = 0
rotation_multiplier = 1.0  # Multiply all angles by this
use_negative_rotation = False  # Toggle between angle and -angle

# Current mode
modes = ["rotation_offset", "x_offset", "y_offset", "rotation_multiplier", "negative_toggle"]
mode_names = ["Rotation Offset", "X Position Offset", "Y Position Offset", "Rotation Multiplier", "Negative Rotation"]
current_mode = 0

def draw_piece(surface, piece_data, rot_offset, x_off, y_off, rot_mult, use_neg):
    """Draw a single piece with adjustments"""
    color = COLORS[piece_data['color']]
    center = [piece_data['center'][0] + x_off, piece_data['center'][1] + y_off]
    angle = piece_data['angle']
    
    # Apply rotation transformations
    angle = angle * rot_mult + rot_offset
    if use_neg:
        angle = -angle
    
    piece_type = piece_data['piece_type']
    
    # Determine size
    if 'large' in piece_type:
        size = 60
    elif 'medium' in piece_type:
        size = 45
    elif 'small' in piece_type:
        size = 30
    else:
        size = 40
    
    # Create surface
    surf_size = size * 3
    surf = pygame.Surface((surf_size, surf_size), pygame.SRCALPHA)
    surf_center = surf_size // 2
    
    # Draw shape
    if 'triangle' in piece_type:
        # RIGHT-ANGLED triangle (matching shape editor)
        points = [
            (surf_center - size//2, surf_center - size//2),  # Top-left (right angle)
            (surf_center + size//2, surf_center - size//2),  # Top-right
            (surf_center - size//2, surf_center + size//2)   # Bottom-left
        ]
        pygame.draw.polygon(surf, color, points, 0)
        pygame.draw.polygon(surf, (255, 255, 255), points, 2)
    elif 'parallelogram' in piece_type:
        # Parallelogram slanting LEFT (matching shape editor)
        points = [
            (surf_center + size//2, surf_center - size//2),
            (surf_center - size//2, surf_center - size//2),
            (surf_center - size - size//2, surf_center + size//2),
            (surf_center - size//2, surf_center + size//2)
        ]
        pygame.draw.polygon(surf, color, points, 0)
        pygame.draw.polygon(surf, (255, 255, 255), points, 2)
    else:  # square
        rect_pos = (surf_center - size//2, surf_center - size//2)
        pygame.draw.rect(surf, color, (*rect_pos, size, size), 0)
        pygame.draw.rect(surf, (255, 255, 255), (*rect_pos, size, size), 2)
    
    # Rotate
    rotated = pygame.transform.rotate(surf, angle)
    rotated_rect = rotated.get_rect(center=center)
    
    surface.blit(rotated, rotated_rect)
    
    # Draw angle label
    label = font_small.render(f"{piece_data['color']} {int(angle)}°", True, (200, 200, 200))
    surface.blit(label, (center[0] + 5, center[1] - 15))

def draw_instructions(surface):
    """Draw control instructions"""
    y = 10
    instructions = [
        f"MODE: {mode_names[current_mode]} (SPACE to change mode)",
        "",
        "ARROW UP/DOWN: Adjust current value",
        "LEFT/RIGHT: Fine adjust (±1)",
        "R: Reset all values",
        "S: Save configuration to file",
        "ESC: Quit",
        "",
        f"Rotation Offset: {rotation_offset}° (add to all angles)",
        f"X Offset: {x_offset} pixels",
        f"Y Offset: {y_offset} pixels",
        f"Rotation Multiplier: {rotation_multiplier:.2f}x",
        f"Use Negative: {use_negative_rotation} (flip rotation direction)",
    ]
    
    for i, text in enumerate(instructions):
        color = (255, 255, 0) if i == 0 else (255, 255, 255)
        label = font.render(text, True, color)
        surface.blit(label, (10, y))
        y += 25

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE:
                current_mode = (current_mode + 1) % len(modes)
            elif event.key == pygame.K_r:
                rotation_offset = 0
                x_offset = 0
                y_offset = 0
                rotation_multiplier = 1.0
                use_negative_rotation = False
                print("Reset all values!")
            elif event.key == pygame.K_s:
                config = {
                    "rotation_offset": rotation_offset,
                    "x_offset": x_offset,
                    "y_offset": y_offset,
                    "rotation_multiplier": rotation_multiplier,
                    "use_negative_rotation": use_negative_rotation
                }
                with open('debug_config.json', 'w') as f:
                    json.dump(config, f, indent=2)
                print(f"\n✓ Saved configuration to debug_config.json")
                print(json.dumps(config, indent=2))
            
            # Adjust current mode value
            elif event.key == pygame.K_UP:
                if modes[current_mode] == "rotation_offset":
                    rotation_offset += 15
                elif modes[current_mode] == "x_offset":
                    x_offset += 10
                elif modes[current_mode] == "y_offset":
                    y_offset += 10
                elif modes[current_mode] == "rotation_multiplier":
                    rotation_multiplier += 0.1
                elif modes[current_mode] == "negative_toggle":
                    use_negative_rotation = not use_negative_rotation
                    
            elif event.key == pygame.K_DOWN:
                if modes[current_mode] == "rotation_offset":
                    rotation_offset -= 15
                elif modes[current_mode] == "x_offset":
                    x_offset -= 10
                elif modes[current_mode] == "y_offset":
                    y_offset -= 10
                elif modes[current_mode] == "rotation_multiplier":
                    rotation_multiplier = max(0.1, rotation_multiplier - 0.1)
                elif modes[current_mode] == "negative_toggle":
                    use_negative_rotation = not use_negative_rotation
                    
            elif event.key == pygame.K_RIGHT:
                if modes[current_mode] == "rotation_offset":
                    rotation_offset += 1
                elif modes[current_mode] == "x_offset":
                    x_offset += 1
                elif modes[current_mode] == "y_offset":
                    y_offset += 1
                elif modes[current_mode] == "rotation_multiplier":
                    rotation_multiplier += 0.01
                    
            elif event.key == pygame.K_LEFT:
                if modes[current_mode] == "rotation_offset":
                    rotation_offset -= 1
                elif modes[current_mode] == "x_offset":
                    x_offset -= 1
                elif modes[current_mode] == "y_offset":
                    y_offset -= 1
                elif modes[current_mode] == "rotation_multiplier":
                    rotation_multiplier = max(0.01, rotation_multiplier - 0.01)
    
    # Clear screen
    screen.fill((40, 40, 40))
    
    # Draw title
    title = font.render("Swan Shape - Interactive Debug", True, (255, 255, 255))
    screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT - 50))
    
    # Draw all pieces
    for piece in SWAN_PIECES:
        draw_piece(screen, piece, rotation_offset, x_offset, y_offset, 
                   rotation_multiplier, use_negative_rotation)
    
    # Draw instructions
    draw_instructions(screen)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
print("\nFinal configuration:")
print(f"  Rotation Offset: {rotation_offset}°")
print(f"  X Offset: {x_offset} px")
print(f"  Y Offset: {y_offset} px")
print(f"  Rotation Multiplier: {rotation_multiplier}x")
print(f"  Use Negative: {use_negative_rotation}")
