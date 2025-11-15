# Tangram Challenge - System Architecture

## Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    TANGRAM CHALLENGE GAME                    │
└─────────────────────────────────────────────────────────────┘

Physical World                Computer Vision              Game Display
─────────────                ──────────────────            ─────────────

┌──────────────┐            ┌──────────────────┐         ┌────────────────┐
│   Physical   │            │  OpenCV Camera   │         │  Pygame Window │
│   Tangram    │──Video────▶│    Detection     │─Data───▶│   Rendering    │
│   Pieces     │            │                  │         │                │
└──────────────┘            └──────────────────┘         └────────────────┘
     (7 colors)                    │                           │
                                   │                           │
                                   ▼                           ▼
                            ┌──────────────┐           ┌──────────────┐
                            │ Color HSV    │           │  Cartoon     │
                            │ Filtering    │           │  Shapes      │
                            └──────────────┘           └──────────────┘
                                   │                           │
                                   ▼                           │
                            ┌──────────────┐                  │
                            │  Contour     │                  │
                            │  Detection   │                  │
                            └──────────────┘                  │
                                   │                           │
                                   ▼                           │
                            ┌──────────────┐                  │
                            │  Position &  │                  │
                            │  Angle       │                  │
                            │  Extraction  │                  │
                            └──────────────┘                  │
                                   │                           │
                                   ▼                           │
                            ┌──────────────┐                  │
                            │  Matching    │                  │
                            │  Algorithm   │                  │
                            └──────────────┘                  │
                                   │                           │
                                   ▼                           │
                            ┌──────────────┐                  │
                            │  Score       │──────────────────┘
                            │  Calculator  │
                            └──────────────┘
```

## Component Details

### 1. TangramDetector (OpenCV)
**Responsibility**: Detect and track physical tangram pieces

**Process**:
1. Capture frame from camera
2. Convert BGR → HSV color space
3. Apply color masks for each of 7 colors
4. Morphological operations (close/open) to clean noise
5. Find contours in each color mask
6. Extract position, angle, area from contours
7. Classify piece type based on dimensions
8. Return list of TangramPiece objects

**Key Methods**:
- `detect_pieces()` → List[TangramPiece]
- `_classify_piece()` → PieceType

### 2. TangramPiece (Data Class)
**Properties**:
- color: str (red, blue, yellow, etc.)
- center: (x, y) position
- angle: rotation in degrees
- contour: OpenCV contour data
- area: pixel area
- piece_type: PieceType enum

### 3. ShapeLibrary (JSON Storage)
**Responsibility**: Manage target shapes

**Data Structure**:
```json
{
  "shape_name": {
    "name": "Display Name",
    "difficulty": "easy|medium|hard",
    "pieces": [
      {
        "color": "red",
        "center": [x, y],
        "angle": degrees,
        "piece_type": "large_triangle"
      },
      ...
    ]
  }
}
```

**Methods**:
- `load_shapes()` → Dict
- `save_shapes()` → void
- `add_shape()` → void

### 4. ScoreCalculator (Matching Algorithm)
**Responsibility**: Calculate match quality

**Algorithm**:
```python
for each target_piece:
    for each detected_piece:
        if colors match:
            # Position score (0-1)
            pos_score = max(0, 1 - distance/100)
            
            # Angle score (0-1)
            angle_diff = min(angle_diff, 360 - angle_diff)
            angle_score = max(0, 1 - angle_diff/180)
            
            # Combined score
            piece_score = (pos_score * 0.6 + angle_score * 0.4) * 100
    
    total_score += best_match_score

final_score = total_score / num_target_pieces
```

**Weights**:
- Position accuracy: 60%
- Angle accuracy: 40%

### 5. TangramGame (Main Game Loop)
**Responsibility**: Orchestrate game flow

**Game Loop**:
```python
while running:
    # 1. Handle input
    handle_events()
    
    # 2. Update state
    if not paused:
        detected_pieces = detector.detect_pieces()
        score = calculator.calculate_match(detected_pieces, target)
    
    # 3. Render
    draw_target_shape()
    draw_detected_pieces()
    draw_info_panel()
    
    # 4. Frame rate
    clock.tick(30)
```

**Layout**:
```
┌────────────────────────────────────────────────────────────┐
│                      Tangram Challenge                      │
├──────────────────────────────┬────────────────────────────┤
│                              │  ┌──────────────────────┐  │
│                              │  │   Score: 73%         │  │
│    Target Shape              │  │   ████████░░░░       │  │
│    (Outline)                 │  └──────────────────────┘  │
│                              │                            │
│         ▲                    │  ┌──────────────────────┐  │
│        ◀■▶  ▼               │  │   Time: 02:45        │  │
│         ●    ◆               │  └──────────────────────┘  │
│                              │                            │
│                              │  Pieces detected: 6/7      │
│    Detected Pieces           │                            │
│    (Cartoon Style)           │  Instructions:             │
│                              │  • SPACE - Pause           │
│        ▲                     │  • R - Reset               │
│       ◀■▶  ▼                │  • N - Next shape          │
│        ●    ◆                │  • ESC - Quit              │
│                              │                            │
└──────────────────────────────┴────────────────────────────┘
```

## Color Detection (HSV)

### Why HSV Instead of RGB?
- More robust to lighting changes
- Easier to define color ranges
- Hue separates color from intensity

### HSV Ranges (Default)
```python
Red:    H: 0-10,   S: 120-255, V: 70-255
Blue:   H: 100-130, S: 120-255, V: 70-255
Yellow: H: 20-30,  S: 120-255, V: 70-255
Green:  H: 40-80,  S: 120-255, V: 70-255
Orange: H: 10-20,  S: 120-255, V: 70-255
Purple: H: 140-170, S: 120-255, V: 70-255
Teal:   H: 85-95,  S: 120-255, V: 70-255
```

### Morphological Operations
```
Original Mask → Close → Open → Clean Mask
      ▼           ▼       ▼         ▼
   Noisy     Fill gaps  Remove   Smooth
             in shapes   noise   contours
```

## Shape Editor Architecture

```
┌─────────────────────────────────────────────────┐
│             Shape Editor Window                  │
├────────────────────────────┬────────────────────┤
│                            │   Pieces Toolbar   │
│                            │  ┌──────────────┐  │
│    Canvas Area             │  │ Large △ Red  │  │
│    (600x600)               │  │ Large △ Blue │  │
│                            │  │ Med △ Orange │  │
│         ▲                  │  │ Small △ Purp │  │
│        ◀■▶  ▼             │  │ Small △ Teal │  │
│         ●    ◆             │  │ Square Yellow│  │
│                            │  │ Parallel Grn │  │
│                            │  └──────────────┘  │
│                            │                    │
│                            │   Controls:        │
│                            │   Click - Add      │
│                            │   Drag - Move      │
│                            │   Right - Rotate   │
│                            │   Del - Remove     │
│                            │   Ctrl+S - Save    │
└────────────────────────────┴────────────────────┘
```

### Editor Features
1. **Piece Library**: Pre-defined pieces with correct colors
2. **Drag & Drop**: Intuitive piece placement
3. **Rotation**: Fine-tuned rotation control
4. **Visual Feedback**: Real-time preview
5. **JSON Export**: Save to shape library

## Performance Considerations

### Optimization Strategies
1. **Frame Rate**: 30 FPS (good balance)
2. **Resolution**: 640x480 (sufficient for detection)
3. **Morphology**: Minimal kernel size (5x5)
4. **Contour Filter**: Area > 500px (remove noise)

### Bottlenecks & Solutions
- **CPU Usage**: Use smaller resolution, reduce morphology iterations
- **Detection Lag**: Optimize HSV ranges, better lighting
- **False Positives**: Stricter area thresholds, better calibration

## Data Flow

```
Camera Frame (BGR)
    ↓
HSV Conversion
    ↓
Color Masking (x7)
    ↓
Morphological Cleaning
    ↓
Contour Detection
    ↓
Feature Extraction
    ↓
TangramPiece Objects
    ↓
Score Calculation ← Target Shape
    ↓
Pygame Rendering
    ↓
User Feedback
```

## Extension Points

### Easy to Add
1. **New Colors**: Add to PIECE_COLORS dict
2. **New Shapes**: Use editor or edit JSON
3. **Difficulty Levels**: Adjust scoring thresholds
4. **Sound Effects**: Add pygame.mixer calls

### Medium Effort
1. **Hint System**: Show piece placement guides
2. **Tutorial Mode**: Step-by-step instructions
3. **Achievements**: Track completed shapes
4. **Multiplayer**: Split-screen with two cameras

### Advanced
1. **Machine Learning**: Train CNN for piece detection
2. **AR Overlay**: Project hints on physical surface
3. **Mobile App**: Port to iOS/Android
4. **Web Version**: WebRTC + JavaScript

## Dependencies

```
opencv-python (4.8+)
├── numpy (1.24+)
└── (video codecs)

pygame (2.5+)
├── SDL2
└── (audio/video libraries)
```

## File Sizes (Approximate)
- tangram_game.py: ~15 KB
- shape_editor.py: ~12 KB
- calibrate_camera.py: ~6 KB
- shapes.json: ~2 KB
- README.md: ~8 KB

## Memory Usage
- OpenCV: ~50-100 MB
- Pygame: ~30-50 MB
- Application: ~10-20 MB
- **Total**: ~100-170 MB

---

This architecture supports the core requirements:
✓ Camera-based detection
✓ Abstract cartoon visualization
✓ Real-time scoring
✓ Shape library
✓ Custom shape creation
✓ Kid-friendly interface
