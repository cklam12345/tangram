"""
Enhanced Tangram Shape Editor
- Right-click drag to move pieces
- Mouse scroll to rotate pieces
- Press 'S' to save current configuration
- Press number keys 1-4 to load preset shapes
- Press 'N' to create new shape
"""

import cv2
import numpy as np
import math
import json
from datetime import datetime

class TangramPiece:
    """Represents a single tangram piece"""
    def __init__(self, piece_type, color, size=100):
        self.type = piece_type
        self.color = color
        self.size = size
        self.x = 400  # Center position
        self.y = 300
        self.rotation = 0  # Degrees
        self.selected = False
        
    def get_vertices(self):
        """Get the vertices of the piece based on type and current transform"""
        if self.type == "large_tri":
            # Right-angled triangle
            base_vertices = np.array([
                [0, 0],
                [self.size, 0],
                [0, self.size]
            ], dtype=np.float32)
        elif self.type == "medium_tri":
            size = self.size * 0.707  # Medium triangle is smaller
            base_vertices = np.array([
                [0, 0],
                [size, 0],
                [0, size]
            ], dtype=np.float32)
        elif self.type == "small_tri":
            size = self.size * 0.5
            base_vertices = np.array([
                [0, 0],
                [size, 0],
                [0, size]
            ], dtype=np.float32)
        elif self.type == "square":
            size = self.size * 0.5
            base_vertices = np.array([
                [0, 0],
                [size, 0],
                [size, size],
                [0, size]
            ], dtype=np.float32)
        elif self.type == "parallelogram":
            size = self.size * 0.5
            # Parallelogram that slants to the LEFT (flipped from normal)
            base_vertices = np.array([
                [size, 0],          # Bottom right
                [0, 0],             # Bottom left
                [-size, size],      # Top left (shifted LEFT by size)
                [0, size]           # Top right
            ], dtype=np.float32)
        else:
            base_vertices = np.array([[0, 0]], dtype=np.float32)
        
        # Center the vertices
        center = np.mean(base_vertices, axis=0)
        centered = base_vertices - center
        
        # Apply rotation
        angle_rad = math.radians(self.rotation)
        cos_a = math.cos(angle_rad)
        sin_a = math.sin(angle_rad)
        rotation_matrix = np.array([
            [cos_a, -sin_a],
            [sin_a, cos_a]
        ])
        rotated = centered @ rotation_matrix.T
        
        # Translate to position
        translated = rotated + np.array([self.x, self.y])
        
        return translated.astype(np.int32)
    
    def contains_point(self, x, y):
        """Check if a point is inside this piece"""
        vertices = self.get_vertices()
        return cv2.pointPolygonTest(vertices, (x, y), False) >= 0


class ShapeEditor:
    """Interactive shape editor for tangram puzzles"""
    
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
        self.canvas = np.ones((height, width, 3), dtype=np.uint8) * 240
        
        # Create the 7 tangram pieces (BGR format for OpenCV!)
        self.pieces = [
            TangramPiece("large_tri", (80, 80, 255)),      # Red - large_tri_1 (BGR: low B, low G, high R)
            TangramPiece("medium_tri", (80, 255, 80)),     # Green - medium_tri (BGR: low B, high G, low R)
            TangramPiece("large_tri", (255, 80, 80)),      # Blue - large_tri_2 (BGR: high B, low G, low R)
            TangramPiece("small_tri", (80, 255, 255)),     # Yellow - small_tri_1 (BGR: low B, high G, high R)
            TangramPiece("small_tri", (255, 80, 255)),     # Magenta - small_tri_2 (BGR: high B, low G, high R)
            TangramPiece("square", (255, 255, 100)),       # Cyan - square (BGR: high B, high G, low R)
            TangramPiece("parallelogram", (0, 128, 255))   # Orange - parallelogram (BGR: low B, mid G, high R)
        ]
        
        # Piece names for saving (matching the order above)
        self.piece_names = [
            "large_tri_1", "medium_tri", "large_tri_2",
            "small_tri_1", "small_tri_2", "square", "parallelogram"
        ]
        
        # Spread pieces out initially
        positions = [
            (200, 200), (600, 200), (400, 150),
            (200, 450), (600, 450), (350, 450), (450, 450)
        ]
        for piece, pos in zip(self.pieces, positions):
            piece.x, piece.y = pos
        
        # Mouse state
        self.selected_piece = None
        self.drag_start = None
        self.current_shape_name = "custom"
        
        # Window name
        self.window_name = "Tangram Shape Editor"
        
    def load_shape(self, shape_name):
        """Load a shape from shapes_config"""
        try:
            from shapes_config import SHAPES, COLOR_MAP, PIECE_TYPE_MAP
            if shape_name not in SHAPES:
                print(f"Shape '{shape_name}' not found!")
                return
            
            shape_data = SHAPES[shape_name]
            pieces_data = shape_data["pieces"]
            
            # Map colors to piece indices
            color_to_index = {
                "red": 0,      # large_tri_1
                "green": 1,    # medium_tri
                "blue": 2,     # large_tri_2
                "yellow": 3,   # small_tri_1
                "purple": 4,   # small_tri_2
                "teal": 5,     # square (using teal/cyan)
                "orange": 6    # parallelogram
            }
            
            for piece_data in pieces_data:
                color = piece_data["color"]
                if color in color_to_index:
                    idx = color_to_index[color]
                    center = piece_data["center"]
                    self.pieces[idx].x = center[0]
                    self.pieces[idx].y = center[1]
                    self.pieces[idx].rotation = piece_data["angle"]
            
            self.current_shape_name = shape_name
            print(f"Loaded shape: {shape_name}")
        except Exception as e:
            print(f"Error loading shape: {e}")
    
    def save_shape(self):
        """Save current configuration to shapes_config.py in the new format"""
        # Color names for each piece
        color_names = ["red", "green", "blue", "yellow", "purple", "teal", "orange"]
        piece_type_names = [
            "large_triangle", "medium_triangle", "large_triangle",
            "small_triangle", "small_triangle", "square", "parallelogram"
        ]
        
        # Get shape name and difficulty from user
        print(f"\nCurrent shape name: '{self.current_shape_name}'")
        print("Enter new shape name (or press Enter to keep current): ", end='')
        new_name = input().strip()
        if new_name:
            self.current_shape_name = new_name
        
        print("Enter difficulty (easy/medium/hard) [default: medium]: ", end='')
        difficulty = input().strip() or "medium"
        
        # Build the shape data in new format
        pieces_data = []
        for i, piece in enumerate(self.pieces):
            pieces_data.append({
                "color": color_names[i],
                "center": [int(piece.x), int(piece.y)],
                "angle": int(piece.rotation % 360),
                "piece_type": piece_type_names[i]
            })
        
        # Build the new shape entry as a formatted string
        shape_str = f'    "{self.current_shape_name}": {{\n'
        shape_str += f'        "name": "{self.current_shape_name.capitalize()}",\n'
        shape_str += f'        "difficulty": "{difficulty}",\n'
        shape_str += '        "pieces": [\n'
        
        for piece_data in pieces_data:
            shape_str += '            {\n'
            shape_str += f'                "color": "{piece_data["color"]}",\n'
            shape_str += f'                "center": {piece_data["center"]},\n'
            shape_str += f'                "angle": {piece_data["angle"]},\n'
            shape_str += f'                "piece_type": "{piece_data["piece_type"]}"\n'
            shape_str += '            },\n'
        
        shape_str += '        ]\n'
        shape_str += '    }'
        
        # Read current config file
        try:
            with open('shapes_config.py', 'r') as f:
                content = f.read()
            
            # Find the SHAPES dictionary
            shapes_start = content.find('SHAPES = {')
            if shapes_start == -1:
                print("Error: Could not find SHAPES dictionary in config file")
                return
            
            # Check if shape already exists
            shape_pattern = f'"{self.current_shape_name}":'
            if shape_pattern in content:
                # Replace existing shape
                print(f"Updating existing shape '{self.current_shape_name}'...")
                # Find the shape entry
                start = content.find(f'"{self.current_shape_name}":')
                if start != -1:
                    # Find the end of this shape
                    brace_count = 0
                    pos = content.find('{', start)
                    end = pos
                    bracket_count = 0
                    in_shape = False
                    
                    while pos < len(content):
                        if content[pos] == '{':
                            brace_count += 1
                            in_shape = True
                        elif content[pos] == '[':
                            bracket_count += 1
                        elif content[pos] == ']':
                            bracket_count -= 1
                        elif content[pos] == '}':
                            brace_count -= 1
                            if brace_count == 0 and bracket_count == 0:
                                end = pos + 1
                                break
                        pos += 1
                    
                    # Find start of the entry (including the key)
                    entry_start = content.rfind('\n', 0, start) + 1
                    # Check if there's a comma after
                    next_newline = content.find('\n', end)
                    if next_newline != -1 and ',' in content[end:next_newline]:
                        end = content.find(',', end) + 1
                    
                    # Replace
                    new_content = content[:entry_start] + shape_str + ',\n' + content[end:]
                    # Remove double commas if any
                    new_content = new_content.replace(',,', ',')
            else:
                # Add new shape
                print(f"Adding new shape '{self.current_shape_name}'...")
                # Find the last closing brace of SHAPES dict
                last_brace = content.rfind('}', 0, content.rfind('}'))
                insert_pos = content.rfind('\n', 0, last_brace) + 1
                new_content = content[:insert_pos] + ',\n\n' + shape_str + '\n' + content[insert_pos:]
                # Clean up formatting
                new_content = new_content.replace(': {,', ': {')
            
            # Write back to file
            with open('shapes_config.py', 'w') as f:
                f.write(new_content)
            
            print(f"✓ Shape '{self.current_shape_name}' saved successfully!")
            
        except Exception as e:
            print(f"Error saving shape: {e}")
            import traceback
            traceback.print_exc()
            # Fallback: save to a JSON file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"shape_{self.current_shape_name}_{timestamp}.json"
            import json
            with open(filename, 'w') as f:
                json.dump({"pieces": pieces_data}, f, indent=2)
            print(f"Saved to backup file: {filename}")
    
    def draw(self):
        """Draw all pieces on the canvas"""
        self.canvas = np.ones((self.height, self.width, 3), dtype=np.uint8) * 240
        
        # Draw grid for reference
        for x in range(0, self.width, 50):
            cv2.line(self.canvas, (x, 0), (x, self.height), (220, 220, 220), 1)
        for y in range(0, self.height, 50):
            cv2.line(self.canvas, (0, y), (self.width, y), (220, 220, 220), 1)
        
        # Draw pieces (non-selected first, then selected on top)
        for piece in self.pieces:
            if not piece.selected:
                vertices = piece.get_vertices()
                color = piece.color
                cv2.fillPoly(self.canvas, [vertices], color)
                cv2.polylines(self.canvas, [vertices], True, (0, 0, 0), 2)
        
        # Draw selected piece on top
        for piece in self.pieces:
            if piece.selected:
                vertices = piece.get_vertices()
                color = tuple(int(c * 0.8) for c in piece.color)  # Darker when selected
                cv2.fillPoly(self.canvas, [vertices], color)
                cv2.polylines(self.canvas, [vertices], True, (255, 255, 0), 3)
        
        # Draw instructions
        instructions = [
            "Right-click drag: Move piece",
            "Mouse scroll: Rotate piece",
            "S: Save shape",
            "1-4: Load preset shapes",
            "N: New shape (clear)",
            "ESC: Quit"
        ]
        
        y_pos = 20
        for instruction in instructions:
            cv2.putText(self.canvas, instruction, (10, y_pos),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (50, 50, 50), 1)
            y_pos += 20
        
        # Show current shape name
        cv2.putText(self.canvas, f"Shape: {self.current_shape_name}", (10, self.height - 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 200), 2)
        
        return self.canvas
    
    def mouse_callback(self, event, x, y, flags, param):
        """Handle mouse events"""
        
        if event == cv2.EVENT_RBUTTONDOWN:
            # Select piece under cursor
            self.drag_start = (x, y)
            for piece in reversed(self.pieces):  # Check top pieces first
                if piece.contains_point(x, y):
                    # Deselect all
                    for p in self.pieces:
                        p.selected = False
                    piece.selected = True
                    self.selected_piece = piece
                    break
        
        elif event == cv2.EVENT_RBUTTONUP:
            self.drag_start = None
        
        elif event == cv2.EVENT_MOUSEMOVE:
            if self.drag_start and self.selected_piece:
                # Move the selected piece
                dx = x - self.drag_start[0]
                dy = y - self.drag_start[1]
                self.selected_piece.x += dx
                self.selected_piece.y += dy
                self.drag_start = (x, y)
        
        elif event == cv2.EVENT_MOUSEWHEEL:
            # Rotate selected piece
            if self.selected_piece:
                if flags > 0:  # Scroll up
                    self.selected_piece.rotation += 15
                else:  # Scroll down
                    self.selected_piece.rotation -= 15
                self.selected_piece.rotation %= 360
    
    def run(self):
        """Run the interactive editor"""
        cv2.namedWindow(self.window_name)
        cv2.setMouseCallback(self.window_name, self.mouse_callback)
        
        print("\n" + "="*50)
        print("TANGRAM SHAPE EDITOR")
        print("="*50)
        print("\nControls:")
        print("  Right-click drag: Move piece")
        print("  Mouse scroll: Rotate piece")
        print("  S: Save shape")
        print("  1-4: Load preset shapes")
        print("  N: New shape (reset)")
        print("  ESC: Quit")
        print("="*50 + "\n")
        
        while True:
            frame = self.draw()
            cv2.imshow(self.window_name, frame)
            
            key = cv2.waitKey(1) & 0xFF
            
            if key == 27:  # ESC
                break
            elif key == ord('s') or key == ord('S'):
                self.save_shape()
            elif key == ord('n') or key == ord('N'):
                self.current_shape_name = "custom"
                print("Creating new shape...")
            elif key == ord('1'):
                self.load_shape("swan")
            elif key == ord('2'):
                self.load_shape("cat")
            elif key == ord('3'):
                self.load_shape("rocket")
            elif key == ord('4'):
                self.load_shape("house")
        
        cv2.destroyAllWindows()


if __name__ == "__main__":
    editor = ShapeEditor()
    editor.run()
