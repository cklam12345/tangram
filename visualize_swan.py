"""
Visualize the swan shape to debug rotation issues
"""
import pygame
import sys

# Import the shape config
from shapes_config import SHAPES

# Initialize Pygame
pygame.init()

# Color mapping (RGB for Pygame)
PYGAME_COLORS = {
    'red': (255, 0, 0),
    'blue': (0, 0, 255),
    'yellow': (255, 255, 0),
    'green': (0, 255, 0),
    'orange': (255, 165, 0),
    'purple': (255, 0, 255),
    'teal': (0, 255, 255),
}

# Create window
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Swan Shape Visualization")

# Get swan shape
swan = SHAPES['swan']

# Draw the swan
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    # Clear screen
    screen.fill((40, 40, 40))
    
    # Title
    font = pygame.font.Font(None, 48)
    title = font.render("Swan Shape - Debug View", True, (255, 255, 255))
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 20))
    
    # Draw each piece
    for piece_data in swan['pieces']:
        color = PYGAME_COLORS[piece_data['color']]
        center = piece_data['center']
        angle = piece_data.get('angle', 0)
        piece_type = piece_data.get('piece_type', '')
        
        # Determine size
        if 'large' in piece_type:
            size = 60
        elif 'medium' in piece_type:
            size = 45
        elif 'small' in piece_type:
            size = 30
        else:
            size = 40
        
        # Create surface for rotation
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
            pygame.draw.polygon(surf, color, points, 0)  # Filled
            pygame.draw.polygon(surf, (255, 255, 255), points, 2)  # White outline
            
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
            pygame.draw.rect(surf, color, (*rect_pos, size, size), 0)  # Filled
            pygame.draw.rect(surf, (255, 255, 255), (*rect_pos, size, size), 2)  # White outline
        
        # Rotate and draw (positive angle = counter-clockwise)
        rotated = pygame.transform.rotate(surf, angle)
        rotated_rect = rotated.get_rect(center=center)
        screen.blit(rotated, rotated_rect)
        
        # Draw center point and label
        pygame.draw.circle(screen, (255, 255, 255), center, 3)
        label_font = pygame.font.Font(None, 20)
        label = label_font.render(f"{piece_data['color']} {angle}°", True, (200, 200, 200))
        screen.blit(label, (center[0] + 10, center[1] - 10))
    
    pygame.display.flip()

pygame.quit()
