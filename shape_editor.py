# -*- coding: utf-8 -*-
"""
Tangram Shape Editor
Create custom animal shapes by placing pieces on the canvas
"""

import pygame
import json
import math
from typing import List, Tuple, Dict, Optional

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
FPS = 60

# Colors
COLORS = {
    'red': (255, 0, 0),
    'blue': (0, 0, 255),
    'yellow': (255, 255, 0),
    'green': (0, 255, 0),
    'orange': (255, 165, 0),
    'purple': (255, 0, 255),
    'teal': (0, 255, 255),
    'white': (255, 255, 255),
    'black': (0, 0, 0),
    'gray': (128, 128, 128),
    'light_gray': (200, 200, 200),
}

PIECE_COLORS = ['red', 'blue', 'yellow', 'green', 'orange', 'purple', 'teal']


class EditorPiece:
    """Represents a piece in the editor"""
    
    def __init__(self, color: str, center: Tuple[float, float], piece_type: str):
        self.color = color
        self.center = list(center)
        self.angle = 0
        self.piece_type = piece_type
        self.selected = False
        self.dragging = False
        self.drag_offset = (0, 0)
        
        # Define piece sizes
        self.sizes = {
            'large_triangle': 80,
            'medium_triangle': 60,
            'small_triangle': 40,
            'square': 50,
            'parallelogram': 50
        }
        self.size = self.sizes.get(piece_type, 50)
    
    def get_vertices(self) -> List[Tuple[float, float]]:
        """Get rotated vertices for drawing"""
        cx, cy = self.center
        angle_rad = math.radians(self.angle)
        
        if 'triangle' in self.piece_type:
            # Equilateral triangle
            s = self.size
            vertices = [
                (0, -s),
                (-s, s),
                (s, s)
            ]
        elif self.piece_type == 'square':
            s = self.size // 2
            vertices = [
                (-s, -s),
                (s, -s),
                (s, s),
                (-s, s)
            ]
        else:  # parallelogram
            s = self.size // 2
            vertices = [
                (-s, -s),
                (s, -s),
                (s + s//2, s),
                (-s + s//2, s)
            ]
        
        # Rotate and translate
        rotated = []
        for x, y in vertices:
            rx = x * math.cos(angle_rad) - y * math.sin(angle_rad)
            ry = x * math.sin(angle_rad) + y * math.cos(angle_rad)
            rotated.append((cx + rx, cy + ry))
        
        return rotated
    
    def contains_point(self, point: Tuple[float, float]) -> bool:
        """Check if point is inside piece"""
        # Simple distance check
        dx = point[0] - self.center[0]
        dy = point[1] - self.center[1]
        dist = math.sqrt(dx*dx + dy*dy)
        return dist < self.size
    
    def draw(self, screen):
        """Draw the piece"""
        vertices = self.get_vertices()
        
        # Draw filled polygon
        pygame.draw.polygon(screen, COLORS[self.color], vertices)
        
        # Draw outline (thicker if selected)
        outline_width = 4 if self.selected else 2
        pygame.draw.polygon(screen, COLORS['white'], vertices, outline_width)
        
        # Draw rotation handle if selected
        if self.selected:
            handle_pos = (
                int(self.center[0]),
                int(self.center[1] - self.size - 15)
            )
            pygame.draw.circle(screen, COLORS['yellow'], handle_pos, 8)
            pygame.draw.line(screen, COLORS['yellow'], 
                           (int(self.center[0]), int(self.center[1])),
                           handle_pos, 2)
    
    def rotate(self, delta_angle: float):
        """Rotate piece by delta degrees"""
        self.angle = (self.angle + delta_angle) % 360
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for saving"""
        return {
            'color': self.color,
            'center': tuple(self.center),
            'angle': self.angle,
            'piece_type': self.piece_type
        }


class ShapeEditor:
    """Main editor class"""
    
    def __init__(self):
        # Initialize display
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Tangram Shape Editor")
        self.clock = pygame.time.Clock()
        
        # Editor state
        self.pieces: List[EditorPiece] = []
        self.selected_piece: Optional[EditorPiece] = None
        self.running = True
        
        # UI elements
        self.font_large = pygame.font.Font(None, 36)
        self.font_medium = pygame.font.Font(None, 28)
        self.font_small = pygame.font.Font(None, 20)
        
        # Layout
        self.canvas_area = pygame.Rect(50, 80, 600, 600)
        self.toolbar_area = pygame.Rect(700, 80, 250, 600)
        
        # Toolbar buttons
        self.piece_buttons = []
        self.create_toolbar()
        
        # Shape metadata
        self.shape_name = "custom_shape"
        self.difficulty = "medium"
        
        # Input state
        self.rotating = False
        self.last_mouse_angle = 0
    
    def create_toolbar(self):
        """Create toolbar with piece templates"""
        piece_types = [
            ('large_triangle', 'Large △'),
            ('large_triangle', 'Large △'),  # Two large triangles
            ('medium_triangle', 'Med △'),
            ('small_triangle', 'Small △'),
            ('small_triangle', 'Small △'),  # Two small triangles
            ('square', 'Square □'),
            ('parallelogram', 'Parallel ▱')
        ]
        
        y = self.toolbar_area.top + 20
        for i, (piece_type, label) in enumerate(piece_types):
            color = PIECE_COLORS[i]
            button = {
                'rect': pygame.Rect(self.toolbar_area.left + 10, y, 230, 50),
                'color': color,
                'piece_type': piece_type,
                'label': label,
                'used': False
            }
            self.piece_buttons.append(button)
            y += 60
    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self.handle_left_click(event.pos)
                elif event.button == 3:  # Right click
                    self.handle_right_click(event.pos)
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.handle_mouse_up()
            
            elif event.type == pygame.MOUSEMOTION:
                self.handle_mouse_motion(event.pos)
            
            elif event.type == pygame.KEYDOWN:
                self.handle_keypress(event.key)
    
    def handle_left_click(self, pos: Tuple[int, int]):
        """Handle left mouse click"""
        # Check toolbar buttons
        for button in self.piece_buttons:
            if button['rect'].collidepoint(pos) and not button['used']:
                # Create new piece
                new_piece = EditorPiece(
                    button['color'],
                    (self.canvas_area.centerx, self.canvas_area.centery),
                    button['piece_type']
                )
                self.pieces.append(new_piece)
                button['used'] = True
                self.select_piece(new_piece)
                return
        
        # Check canvas pieces
        if self.canvas_area.collidepoint(pos):
            # Check rotation handle first
            if self.selected_piece:
                handle_pos = (
                    self.selected_piece.center[0],
                    self.selected_piece.center[1] - self.selected_piece.size - 15
                )
                dx = pos[0] - handle_pos[0]
                dy = pos[1] - handle_pos[1]
                if math.sqrt(dx*dx + dy*dy) < 10:
                    self.rotating = True
                    self.last_mouse_angle = math.atan2(
                        pos[1] - self.selected_piece.center[1],
                        pos[0] - self.selected_piece.center[0]
                    )
                    return
            
            # Check pieces (reverse order for top-first selection)
            for piece in reversed(self.pieces):
                if piece.contains_point(pos):
                    self.select_piece(piece)
                    piece.dragging = True
                    piece.drag_offset = (
                        pos[0] - piece.center[0],
                        pos[1] - piece.center[1]
                    )
                    return
            
            # Clicked empty space - deselect
            self.selected_piece = None
            for piece in self.pieces:
                piece.selected = False
    
    def handle_right_click(self, pos: Tuple[int, int]):
        """Handle right mouse click (rotate 15 degrees)"""
        if self.canvas_area.collidepoint(pos):
            for piece in reversed(self.pieces):
                if piece.contains_point(pos):
                    piece.rotate(15)
                    return
    
    def handle_mouse_up(self):
        """Handle mouse button release"""
        for piece in self.pieces:
            piece.dragging = False
        self.rotating = False
    
    def handle_mouse_motion(self, pos: Tuple[int, int]):
        """Handle mouse movement"""
        if self.rotating and self.selected_piece:
            # Calculate rotation
            angle = math.atan2(
                pos[1] - self.selected_piece.center[1],
                pos[0] - self.selected_piece.center[0]
            )
            delta = math.degrees(angle - self.last_mouse_angle)
            self.selected_piece.rotate(delta)
            self.last_mouse_angle = angle
        
        elif self.selected_piece and self.selected_piece.dragging:
            # Drag piece
            self.selected_piece.center[0] = pos[0] - self.selected_piece.drag_offset[0]
            self.selected_piece.center[1] = pos[1] - self.selected_piece.drag_offset[1]
            
            # Keep within canvas
            margin = self.selected_piece.size
            self.selected_piece.center[0] = max(
                self.canvas_area.left + margin,
                min(self.canvas_area.right - margin, self.selected_piece.center[0])
            )
            self.selected_piece.center[1] = max(
                self.canvas_area.top + margin,
                min(self.canvas_area.bottom - margin, self.selected_piece.center[1])
            )
    
    def handle_keypress(self, key):
        """Handle keyboard input"""
        if key == pygame.K_ESCAPE:
            self.running = False
        elif key == pygame.K_DELETE and self.selected_piece:
            self.delete_selected_piece()
        elif key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
            self.save_shape()
        elif key == pygame.K_c:
            self.clear_canvas()
        elif key == pygame.K_LEFT and self.selected_piece:
            self.selected_piece.rotate(-5)
        elif key == pygame.K_RIGHT and self.selected_piece:
            self.selected_piece.rotate(5)
    
    def select_piece(self, piece: EditorPiece):
        """Select a piece"""
        for p in self.pieces:
            p.selected = False
        piece.selected = True
        self.selected_piece = piece
    
    def delete_selected_piece(self):
        """Delete the selected piece"""
        if self.selected_piece:
            # Mark button as unused
            for button in self.piece_buttons:
                if (button['color'] == self.selected_piece.color and
                    button['piece_type'] == self.selected_piece.piece_type):
                    button['used'] = False
                    break
            
            self.pieces.remove(self.selected_piece)
            self.selected_piece = None
    
    def clear_canvas(self):
        """Clear all pieces"""
        self.pieces.clear()
        self.selected_piece = None
        for button in self.piece_buttons:
            button['used'] = False
    
    def save_shape(self):
        """Save current shape to library"""
        if len(self.pieces) != 7:
            print(f"Warning: Shape should have 7 pieces, has {len(self.pieces)}")
        
        shape_data = {
            'name': self.shape_name,
            'difficulty': self.difficulty,
            'pieces': [piece.to_dict() for piece in self.pieces]
        }
        
        # Load existing shapes
        try:
            with open('shapes.json', 'r', encoding='utf-8') as f:
                shapes = json.load(f)
        except FileNotFoundError:
            shapes = {}
        
        # Add new shape
        shapes[self.shape_name.lower().replace(' ', '_')] = shape_data
        
        # Save
        with open('shapes.json', 'w', encoding='utf-8') as f:
            json.dump(shapes, f, indent=2, ensure_ascii=False)
        
        print(f"Shape '{self.shape_name}' saved successfully!")
    
    def draw(self):
        """Draw everything"""
        # Clear screen
        self.screen.fill(COLORS['black'])
        
        # Draw title
        title = self.font_large.render("Tangram Shape Editor", True, COLORS['white'])
        self.screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, 20))
        
        # Draw canvas
        pygame.draw.rect(self.screen, (40, 40, 40), self.canvas_area)
        pygame.draw.rect(self.screen, COLORS['white'], self.canvas_area, 3)
        
        # Draw pieces
        for piece in self.pieces:
            piece.draw(self.screen)
        
        # Draw toolbar
        pygame.draw.rect(self.screen, COLORS['light_gray'], self.toolbar_area)
        pygame.draw.rect(self.screen, COLORS['gray'], self.toolbar_area, 3)
        
        toolbar_title = self.font_medium.render("Pieces", True, COLORS['black'])
        self.screen.blit(toolbar_title, (self.toolbar_area.left + 10, self.toolbar_area.top - 30))
        
        # Draw piece buttons
        for button in self.piece_buttons:
            color = COLORS['gray'] if button['used'] else COLORS[button['color']]
            pygame.draw.rect(self.screen, color, button['rect'])
            pygame.draw.rect(self.screen, COLORS['black'], button['rect'], 2)
            
            label = self.font_small.render(button['label'], True, COLORS['white'])
            label_pos = (
                button['rect'].centerx - label.get_width() // 2,
                button['rect'].centery - label.get_height() // 2
            )
            self.screen.blit(label, label_pos)
        
        # Draw instructions
        y = self.toolbar_area.bottom - 180
        instructions = [
            "Controls:",
            "Left Click - Select/Drag",
            "Right Click - Rotate 15°",
            "Arrow Keys - Rotate 5°",
            "Delete - Remove piece",
            "C - Clear all",
            "Ctrl+S - Save shape",
            "ESC - Quit"
        ]
        
        for instruction in instructions:
            text = self.font_small.render(instruction, True, COLORS['black'])
            self.screen.blit(text, (self.toolbar_area.left + 10, y))
            y += 22
        
        pygame.display.flip()
    
    def run(self):
        """Main editor loop"""
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()


def main():
    """Entry point"""
    print("Tangram Shape Editor")
    print("Create custom shapes by arranging the 7 tangram pieces!")
    print("\nControls:")
    print("  Left Click - Select and drag pieces")
    print("  Right Click - Rotate piece 15 degrees")
    print("  Arrow Keys - Fine rotate selected piece")
    print("  Delete - Remove selected piece")
    print("  C - Clear canvas")
    print("  Ctrl+S - Save shape")
    print("  ESC - Quit")
    print("\nStarting editor...")
    
    editor = ShapeEditor()
    editor.run()


if __name__ == "__main__":
    main()
