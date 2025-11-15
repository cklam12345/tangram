"""
Tangram Game - OpenCV piece detection with Pygame visualization
Detects 7 colored tangram pieces and matches them to target shapes
"""

import cv2
import numpy as np
import pygame
import json
import time
from dataclasses import dataclass
from typing import List, Tuple, Dict
from enum import Enum

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
FPS = 30

# Tangram piece colors (BGR format for OpenCV)
PIECE_COLORS = {
    'red': {'bgr': (0, 0, 255), 'hsv_lower': np.array([0, 120, 70]), 'hsv_upper': np.array([10, 255, 255])},
    'blue': {'bgr': (255, 0, 0), 'hsv_lower': np.array([100, 120, 70]), 'hsv_upper': np.array([130, 255, 255])},
    'yellow': {'bgr': (0, 255, 255), 'hsv_lower': np.array([20, 120, 70]), 'hsv_upper': np.array([30, 255, 255])},
    'green': {'bgr': (0, 255, 0), 'hsv_lower': np.array([40, 120, 70]), 'hsv_upper': np.array([80, 255, 255])},
    'orange': {'bgr': (0, 165, 255), 'hsv_lower': np.array([10, 120, 70]), 'hsv_upper': np.array([20, 255, 255])},
    'purple': {'bgr': (255, 0, 255), 'hsv_lower': np.array([140, 120, 70]), 'hsv_upper': np.array([170, 255, 255])},
    'teal': {'bgr': (255, 255, 0), 'hsv_lower': np.array([85, 120, 70]), 'hsv_upper': np.array([95, 255, 255])},
}

# Pygame colors
PYGAME_COLORS = {
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


class PieceType(Enum):
    LARGE_TRIANGLE = "large_triangle"
    MEDIUM_TRIANGLE = "medium_triangle"
    SMALL_TRIANGLE = "small_triangle"
    SQUARE = "square"
    PARALLELOGRAM = "parallelogram"


@dataclass
class TangramPiece:
    """Represents a detected tangram piece"""
    color: str
    center: Tuple[float, float]
    angle: float  # in degrees
    contour: np.ndarray
    area: float
    piece_type: PieceType = None
    
    def to_dict(self):
        return {
            'color': self.color,
            'center': self.center,
            'angle': self.angle,
            'area': self.area
        }


@dataclass
class TargetPiece:
    """Represents a piece in the target shape"""
    color: str
    center: Tuple[float, float]
    angle: float
    piece_type: PieceType
    
    def to_dict(self):
        return {
            'color': self.color,
            'center': self.center,
            'angle': self.angle,
            'piece_type': self.piece_type.value
        }


class TangramDetector:
    """Detects tangram pieces using OpenCV"""
    
    def __init__(self, camera_id=0):
        self.cap = cv2.VideoCapture(camera_id)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
    def detect_pieces(self) -> List[TangramPiece]:
        """Detect all tangram pieces in the current frame"""
        ret, frame = self.cap.read()
        if not ret:
            return []
        
        # Convert to HSV for better color detection
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        pieces = []
        
        for color_name, color_data in PIECE_COLORS.items():
            # Create mask for this color
            mask = cv2.inRange(hsv, color_data['hsv_lower'], color_data['hsv_upper'])
            
            # Clean up mask
            kernel = np.ones((5, 5), np.uint8)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            
            # Find contours
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                area = cv2.contourArea(contour)
                
                # Filter out small noise
                if area < 500:
                    continue
                
                # Get minimum area rectangle
                rect = cv2.minAreaRect(contour)
                center, (width, height), angle = rect
                
                # Normalize angle to 0-360
                angle = angle % 360
                
                piece = TangramPiece(
                    color=color_name,
                    center=center,
                    angle=angle,
                    contour=contour,
                    area=area
                )
                
                # Classify piece type based on area (approximate)
                piece.piece_type = self._classify_piece(area, width, height)
                
                pieces.append(piece)
        
        return pieces
    
    def _classify_piece(self, area, width, height):
        """Classify piece type based on dimensions"""
        aspect_ratio = max(width, height) / (min(width, height) + 0.001)
        
        if aspect_ratio > 1.3:  # Triangular or parallelogram
            if area > 8000:
                return PieceType.LARGE_TRIANGLE
            elif area > 4000:
                return PieceType.MEDIUM_TRIANGLE
            else:
                return PieceType.SMALL_TRIANGLE
        else:  # More square-like
            return PieceType.SQUARE
    
    def get_frame(self):
        """Get current camera frame for debugging"""
        ret, frame = self.cap.read()
        return frame if ret else None
    
    def release(self):
        """Release camera resources"""
        self.cap.release()


class ShapeLibrary:
    """Manages target shapes and patterns"""
    
    def __init__(self, filename='shapes.json'):
        self.filename = filename
        self.shapes = self.load_shapes()
        
    def load_shapes(self) -> Dict:
        """Load shapes from JSON file"""
        try:
            with open(self.filename, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Create default shapes
            return self.create_default_shapes()
    
    def create_default_shapes(self) -> Dict:
        """Create default shape library including the swan"""
        shapes = {
            'swan': {
                'name': 'Swan',
                'difficulty': 'medium',
                'pieces': [
                    {'color': 'red', 'center': (200, 300), 'angle': 0, 'piece_type': 'large_triangle'},
                    {'color': 'blue', 'center': (300, 250), 'angle': 45, 'piece_type': 'large_triangle'},
                    {'color': 'green', 'center': (400, 300), 'angle': 90, 'piece_type': 'large_triangle'},
                    {'color': 'orange', 'center': (280, 150), 'angle': 45, 'piece_type': 'medium_triangle'},
                    {'color': 'yellow', 'center': (310, 180), 'angle': 0, 'piece_type': 'square'},
                    {'color': 'teal', 'center': (330, 220), 'angle': 45, 'piece_type': 'small_triangle'},
                    {'color': 'purple', 'center': (350, 120), 'angle': 90, 'piece_type': 'small_triangle'},
                ]
            },
            'cat': {
                'name': 'Cat',
                'difficulty': 'easy',
                'pieces': [
                    {'color': 'red', 'center': (250, 300), 'angle': 0, 'piece_type': 'large_triangle'},
                    {'color': 'blue', 'center': (350, 300), 'angle': 0, 'piece_type': 'large_triangle'},
                    {'color': 'green', 'center': (300, 200), 'angle': 45, 'piece_type': 'medium_triangle'},
                    {'color': 'yellow', 'center': (300, 250), 'angle': 0, 'piece_type': 'square'},
                    {'color': 'orange', 'center': (220, 180), 'angle': 45, 'piece_type': 'small_triangle'},
                    {'color': 'purple', 'center': (380, 180), 'angle': 135, 'piece_type': 'small_triangle'},
                    {'color': 'teal', 'center': (300, 150), 'angle': 0, 'piece_type': 'parallelogram'},
                ]
            },
            'rocket': {
                'name': 'Rocket',
                'difficulty': 'hard',
                'pieces': [
                    {'color': 'red', 'center': (300, 350), 'angle': 0, 'piece_type': 'large_triangle'},
                    {'color': 'blue', 'center': (300, 250), 'angle': 0, 'piece_type': 'large_triangle'},
                    {'color': 'green', 'center': (300, 150), 'angle': 0, 'piece_type': 'medium_triangle'},
                    {'color': 'yellow', 'center': (300, 200), 'angle': 0, 'piece_type': 'square'},
                    {'color': 'orange', 'center': (250, 380), 'angle': 45, 'piece_type': 'small_triangle'},
                    {'color': 'purple', 'center': (350, 380), 'angle': 135, 'piece_type': 'small_triangle'},
                    {'color': 'teal', 'center': (300, 100), 'angle': 0, 'piece_type': 'small_triangle'},
                ]
            }
        }
        self.save_shapes(shapes)
        return shapes
    
    def save_shapes(self, shapes=None):
        """Save shapes to JSON file"""
        if shapes is None:
            shapes = self.shapes
        with open(self.filename, 'w') as f:
            json.dump(shapes, f, indent=2)
    
    def add_shape(self, name, pieces, difficulty='medium'):
        """Add a new shape to the library"""
        self.shapes[name.lower()] = {
            'name': name,
            'difficulty': difficulty,
            'pieces': [p if isinstance(p, dict) else p.to_dict() for p in pieces]
        }
        self.save_shapes()


class ScoreCalculator:
    """Calculates matching score between detected and target pieces"""
    
    @staticmethod
    def calculate_match(detected: List[TangramPiece], target: List[Dict]) -> float:
        """
        Calculate matching score (0-100)
        Based on position and angle accuracy
        """
        if not detected or not target:
            return 0.0
        
        total_score = 0.0
        matched_count = 0
        
        for target_piece in target:
            best_match_score = 0.0
            
            for detected_piece in detected:
                # Match by color first
                if detected_piece.color != target_piece['color']:
                    continue
                
                # Calculate position difference (normalized)
                pos_diff = np.sqrt(
                    (detected_piece.center[0] - target_piece['center'][0])**2 +
                    (detected_piece.center[1] - target_piece['center'][1])**2
                )
                
                # Position score (inverse of distance, max distance = 100 pixels)
                pos_score = max(0, 100 - pos_diff) / 100.0
                
                # Calculate angle difference (normalized to 0-180)
                angle_diff = abs(detected_piece.angle - target_piece['angle'])
                angle_diff = min(angle_diff, 360 - angle_diff)
                
                # Angle score (allow 15 degree tolerance)
                angle_score = max(0, 1 - angle_diff / 180.0)
                
                # Combined score (weighted average)
                piece_score = (pos_score * 0.6 + angle_score * 0.4) * 100
                
                best_match_score = max(best_match_score, piece_score)
            
            if best_match_score > 30:  # Minimum threshold to count as matched
                total_score += best_match_score
                matched_count += 1
        
        # Average score across all target pieces
        return total_score / len(target) if target else 0.0


class TangramGame:
    """Main game class managing the entire application"""
    
    def __init__(self):
        # Initialize display
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Tangram Challenge")
        self.clock = pygame.time.Clock()
        
        # Initialize components
        self.detector = TangramDetector()
        self.shape_library = ShapeLibrary()
        self.score_calculator = ScoreCalculator()
        
        # Game state
        self.current_shape = 'swan'
        self.detected_pieces = []
        self.score = 0.0
        self.start_time = time.time()
        self.game_duration = 180  # 3 minutes
        self.running = True
        self.paused = False
        
        # UI elements
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        # Layout
        self.game_area = pygame.Rect(50, 100, 700, 650)
        self.info_area = pygame.Rect(800, 100, 350, 650)
        
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                elif event.key == pygame.K_r:
                    self.reset_game()
                elif event.key == pygame.K_n:
                    self.next_shape()
    
    def update(self):
        """Update game state"""
        if self.paused:
            return
        
        # Detect pieces from camera
        self.detected_pieces = self.detector.detect_pieces()
        
        # Calculate score
        target_pieces = self.shape_library.shapes[self.current_shape]['pieces']
        self.score = self.score_calculator.calculate_match(self.detected_pieces, target_pieces)
    
    def draw_target_shape(self):
        """Draw the target shape outline"""
        target_data = self.shape_library.shapes[self.current_shape]
        
        # Draw title
        title_text = self.font_large.render(f"Make a {target_data['name']}!", True, PYGAME_COLORS['white'])
        self.screen.blit(title_text, (self.game_area.centerx - title_text.get_width()//2, 20))
        
        # Draw target pieces as cute cartoon shapes
        for piece_data in target_data['pieces']:
            color = PYGAME_COLORS[piece_data['color']]
            center = piece_data['center']
            
            # Draw as simple shapes with outline
            if 'triangle' in piece_data.get('piece_type', ''):
                # Draw triangle
                size = 40 if 'large' in piece_data.get('piece_type', '') else 25
                points = [
                    (center[0], center[1] - size),
                    (center[0] - size, center[1] + size),
                    (center[0] + size, center[1] + size)
                ]
                pygame.draw.polygon(self.screen, color, points, 3)
            else:
                # Draw square/parallelogram
                size = 30
                pygame.draw.rect(self.screen, color, 
                               (center[0]-size//2, center[1]-size//2, size, size), 3)
    
    def draw_detected_pieces(self):
        """Draw detected pieces as cartoon representations"""
        for piece in self.detected_pieces:
            color = PYGAME_COLORS[piece.color]
            center = (int(piece.center[0]) + self.game_area.left, 
                     int(piece.center[1]) + self.game_area.top)
            
            # Draw filled cartoon shape
            if piece.piece_type and 'triangle' in piece.piece_type.value:
                size = 35 if 'large' in piece.piece_type.value else 20
                points = [
                    (center[0], center[1] - size),
                    (center[0] - size, center[1] + size),
                    (center[0] + size, center[1] + size)
                ]
                pygame.draw.polygon(self.screen, color, points)
                pygame.draw.polygon(self.screen, PYGAME_COLORS['white'], points, 2)
            else:
                size = 25
                pygame.draw.rect(self.screen, color, 
                               (center[0]-size//2, center[1]-size//2, size, size))
                pygame.draw.rect(self.screen, PYGAME_COLORS['white'],
                               (center[0]-size//2, center[1]-size//2, size, size), 2)
    
    def draw_info_panel(self):
        """Draw information panel with score and timer"""
        # Background
        pygame.draw.rect(self.screen, PYGAME_COLORS['light_gray'], self.info_area)
        pygame.draw.rect(self.screen, PYGAME_COLORS['gray'], self.info_area, 3)
        
        y_offset = self.info_area.top + 20
        
        # Score
        score_text = self.font_large.render(f"Score: {int(self.score)}%", True, PYGAME_COLORS['black'])
        self.screen.blit(score_text, (self.info_area.left + 20, y_offset))
        y_offset += 70
        
        # Progress bar
        bar_width = 300
        bar_height = 30
        bar_rect = pygame.Rect(self.info_area.left + 25, y_offset, bar_width, bar_height)
        pygame.draw.rect(self.screen, PYGAME_COLORS['white'], bar_rect)
        fill_width = int(bar_width * (self.score / 100))
        fill_rect = pygame.Rect(self.info_area.left + 25, y_offset, fill_width, bar_height)
        
        # Color based on score
        if self.score >= 80:
            bar_color = (0, 255, 0)
        elif self.score >= 50:
            bar_color = (255, 165, 0)
        else:
            bar_color = (255, 0, 0)
        
        pygame.draw.rect(self.screen, bar_color, fill_rect)
        pygame.draw.rect(self.screen, PYGAME_COLORS['black'], bar_rect, 2)
        y_offset += 60
        
        # Timer
        elapsed = time.time() - self.start_time
        remaining = max(0, self.game_duration - elapsed)
        minutes = int(remaining // 60)
        seconds = int(remaining % 60)
        
        timer_text = self.font_medium.render(f"Time: {minutes:02d}:{seconds:02d}", True, PYGAME_COLORS['black'])
        self.screen.blit(timer_text, (self.info_area.left + 20, y_offset))
        y_offset += 60
        
        # Detected pieces count
        count_text = self.font_small.render(f"Pieces detected: {len(self.detected_pieces)}/7", 
                                           True, PYGAME_COLORS['black'])
        self.screen.blit(count_text, (self.info_area.left + 20, y_offset))
        y_offset += 80
        
        # Instructions
        instructions = [
            "Instructions:",
            "",
            "Arrange the colored",
            "tangram pieces to",
            "match the target shape!",
            "",
            "Controls:",
            "SPACE - Pause",
            "R - Reset",
            "N - Next shape",
            "ESC - Quit"
        ]
        
        for instruction in instructions:
            text = self.font_small.render(instruction, True, PYGAME_COLORS['black'])
            self.screen.blit(text, (self.info_area.left + 20, y_offset))
            y_offset += 30
    
    def draw(self):
        """Draw everything"""
        # Clear screen
        self.screen.fill(PYGAME_COLORS['black'])
        
        # Draw game area background
        pygame.draw.rect(self.screen, (40, 40, 40), self.game_area)
        pygame.draw.rect(self.screen, PYGAME_COLORS['white'], self.game_area, 3)
        
        # Draw target shape
        self.draw_target_shape()
        
        # Draw detected pieces
        self.draw_detected_pieces()
        
        # Draw info panel
        self.draw_info_panel()
        
        # Draw pause overlay
        if self.paused:
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))
            
            pause_text = self.font_large.render("PAUSED", True, PYGAME_COLORS['white'])
            self.screen.blit(pause_text, 
                           (WINDOW_WIDTH//2 - pause_text.get_width()//2,
                            WINDOW_HEIGHT//2 - pause_text.get_height()//2))
        
        # Victory check
        if self.score >= 85:
            victory_text = self.font_large.render("GREAT JOB!", True, (255, 215, 0))
            self.screen.blit(victory_text,
                           (self.game_area.centerx - victory_text.get_width()//2,
                            self.game_area.centery - 50))
        
        pygame.display.flip()
    
    def reset_game(self):
        """Reset game state"""
        self.start_time = time.time()
        self.score = 0.0
    
    def next_shape(self):
        """Switch to next shape"""
        shapes = list(self.shape_library.shapes.keys())
        current_index = shapes.index(self.current_shape)
        self.current_shape = shapes[(current_index + 1) % len(shapes)]
        self.reset_game()
    
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        self.detector.release()
        pygame.quit()


def main():
    """Entry point"""
    print("Starting Tangram Challenge Game...")
    print("Make sure your camera is positioned to view the desktop from above!")
    print("\nControls:")
    print("  SPACE - Pause/Resume")
    print("  R - Reset timer")
    print("  N - Next shape")
    print("  ESC - Quit")
    print("\nStarting in 3 seconds...")
    time.sleep(3)
    
    game = TangramGame()
    game.run()


if __name__ == "__main__":
    main()
