"""
Debug script to verify rotation angles are loaded and applied correctly
"""

# First, let's manually create a clean config without the syntax error
SHAPES = {
    "swan": {
        "name": "Swan",
        "difficulty": "medium",
        "pieces": [
            {
                "color": "red",
                "center": [305, 290],
                "angle": 225,
                "piece_type": "large_triangle"
            },
            {
                "color": "green",
                "center": [401, 320],
                "angle": 135,
                "piece_type": "medium_triangle"
            },
            {
                "color": "blue",
                "center": [346, 335],
                "angle": 180,
                "piece_type": "large_triangle"
            },
            {
                "color": "yellow",
                "center": [426, 280],
                "angle": 315,
                "piece_type": "small_triangle"
            },
            {
                "color": "purple",
                "center": [418, 165],
                "angle": 270,
                "piece_type": "small_triangle"
            },
            {
                "color": "teal",
                "center": [399, 241],
                "angle": 315,
                "piece_type": "square"
            },
            {
                "color": "orange",
                "center": [378, 186],
                "angle": 315,
                "piece_type": "parallelogram"
            }
        ]
    }
}

print("="*60)
print("SWAN SHAPE ROTATION DEBUG")
print("="*60)

swan = SHAPES['swan']
print(f"\nShape: {swan['name']}")
print(f"Pieces: {len(swan['pieces'])}")
print()

for i, piece in enumerate(swan['pieces'], 1):
    print(f"{i}. {piece['color']:8s} {piece['piece_type']:18s} at ({piece['center'][0]:3d}, {piece['center'][1]:3d}) rotated {piece['angle']:3d}°")

print("\n" + "="*60)
print("ROTATION ANGLE INTERPRETATION")
print("="*60)
print()
print("In Pygame, rotation works like this:")
print("  - 0° = shape points UP (default)")
print("  - 90° = shape points LEFT")
print("  - 180° = shape points DOWN")
print("  - 270° = shape points RIGHT")
print("  - Negative rotation in pygame.transform.rotate() means CLOCKWISE")
print()
print("Your config angles:")
print("  red (225°)    -> Should point LOWER-LEFT")
print("  green (135°)  -> Should point UPPER-LEFT")
print("  blue (180°)   -> Should point DOWN")
print("  yellow (315°) -> Should point LOWER-RIGHT")
print("  purple (270°) -> Should point RIGHT")
print("  teal (315°)   -> Should point LOWER-RIGHT")
print("  orange (315°) -> Should point LOWER-RIGHT")
print()

# Now test if pygame rotation works as expected
import pygame
pygame.init()

print("="*60)
print("TESTING PYGAME ROTATION")
print("="*60)

# Create a simple test
screen = pygame.display.set_mode((400, 400))
pygame.display.set_caption("Rotation Test")

# Draw a triangle at different angles
font = pygame.font.Font(None, 24)

test_angles = [0, 45, 90, 135, 180, 225, 270, 315]
positions = [
    (100, 100), (200, 100), (300, 100),
    (100, 200), (200, 200), (300, 200),
    (100, 300), (200, 300)
]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
    
    screen.fill((40, 40, 40))
    
    title = font.render("Triangle Rotation Test - ESC to close", True, (255, 255, 255))
    screen.blit(title, (10, 10))
    
    for angle, pos in zip(test_angles, positions):
        # Create surface
        surf = pygame.Surface((80, 80), pygame.SRCALPHA)
        
        # Draw triangle pointing UP
        points = [(40, 10), (10, 70), (70, 70)]
        pygame.draw.polygon(surf, (255, 0, 0), points, 0)
        pygame.draw.polygon(surf, (255, 255, 255), points, 2)
        
        # Rotate
        rotated = pygame.transform.rotate(surf, -angle)  # Negative for clockwise
        rect = rotated.get_rect(center=pos)
        
        screen.blit(rotated, rect)
        
        # Label
        label = font.render(f"{angle}°", True, (255, 255, 0))
        screen.blit(label, (pos[0] - 15, pos[1] + 35))
    
    pygame.display.flip()

pygame.quit()

print("\n✓ Rotation test complete!")
print("\nDid you see the triangles rotate correctly?")
print("If yes, then the game SHOULD be applying your angles correctly.")
print("If not, there's an issue with how pygame.transform.rotate works.")
