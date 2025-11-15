# Tangram Challenge Game

An interactive tangram puzzle game that uses computer vision (OpenCV) to detect physical tangram pieces and provides real-time scoring through a fun Pygame interface.

## Features

🎮 **Real-time Detection**: Uses your PC camera to detect and track 7 colored tangram pieces  
🎨 **Cartoon Visualization**: Abstract, kid-friendly representation of pieces (no camera feed shown)  
📚 **Shape Library**: Multiple animal shapes including swan, cat, and rocket  
✏️ **Shape Editor**: Create custom shapes to challenge kids  
⏱️ **Timed Scoring**: Real-time scoring system with timer  
🎯 **Progressive Difficulty**: Different difficulty levels for different ages

## How It Works

1. **Camera Setup**: Position your PC camera facing down at your desktop at an angle
2. **Piece Detection**: OpenCV detects the 7 colored tangram pieces using HSV color detection
3. **Visual Feedback**: Pieces are displayed as cartoon shapes on screen (camera view is hidden)
4. **Real-time Scoring**: As pieces move closer to the target shape, score increases
5. **Kid-Friendly Interface**: Bright colors, simple shapes, encouraging feedback

## Tangram Pieces

The game uses 7 standard tangram pieces in different colors:
- 🔴 Red - Large Triangle
- 🔵 Blue - Large Triangle  
- 🟢 Green - Large Triangle
- 🟠 Orange - Medium Triangle
- 🟡 Yellow - Square
- 🟣 Purple - Small Triangle
- 🔵 Teal - Small Triangle

## Installation

### Requirements
- Python 3.8+
- Webcam/PC camera
- Physical tangram pieces in the specified colors

### Setup

1. Clone or download this repository

2. Install dependencies:
```bash
pip install opencv-python numpy pygame
```

3. Position your camera:
   - Mount camera facing desktop from above or at an angle
   - Ensure good lighting
   - White or light-colored desktop background works best

4. (Optional) Calibrate colors:
```bash
python calibrate_camera.py
```
   - Use this tool to fine-tune color detection for your lighting
   - Press 1-7 to switch between colors
   - Adjust HSV sliders until piece is clearly detected
   - Press 's' to save calibration

## Usage

### Playing the Game

```bash
python tangram_game.py
```

**Controls:**
- `SPACE` - Pause/Resume
- `R` - Reset timer
- `N` - Next shape
- `ESC` - Quit

**Gameplay:**
1. Place your tangram pieces on the desktop
2. Look at the target shape on screen
3. Arrange your physical pieces to match the target
4. Watch your score increase as pieces align!
5. Try to get 85%+ score to win

### Creating Custom Shapes

```bash
python shape_editor.py
```

**Editor Controls:**
- `Left Click` - Select and drag pieces
- `Right Click` - Rotate piece 15°
- `Arrow Keys` - Fine rotate selected piece (5°)
- `Delete` - Remove selected piece
- `C` - Clear all pieces
- `Ctrl+S` - Save shape to library
- `ESC` - Quit

**Creating a Shape:**
1. Click piece buttons on the right to add them to canvas
2. Drag pieces to position them
3. Rotate pieces by right-clicking or using arrow keys
4. Arrange all 7 pieces into your desired shape
5. Press Ctrl+S to save to the shape library
6. Your shape will now appear in the game!

## File Structure

```
tangram_game/
├── tangram_game.py          # Main game application
├── shape_editor.py          # Shape creation tool
├── calibrate_camera.py      # Color calibration utility
├── shapes.json              # Shape library (auto-generated)
├── color_calibration.json   # Custom color ranges (optional)
└── README.md               # This file
```

## Tips for Best Results

### Camera Setup
- Position camera 1-2 feet above desktop
- Angle slightly for better view
- Ensure even lighting (avoid shadows)
- Use a light-colored, plain desktop surface

### Piece Selection
- Use bright, solid-colored tangram pieces
- Ensure colors match the defined palette
- Pieces should be opaque (not translucent)
- Larger pieces are easier to detect

### Gameplay
- Start with easier shapes (cat) before harder ones (rocket)
- Keep pieces flat on the surface
- Avoid overlapping pieces
- Move pieces slowly for better detection

## Troubleshooting

### Pieces Not Detected
1. Run `calibrate_camera.py` to adjust color ranges
2. Improve lighting conditions
3. Check camera is working and positioned correctly
4. Ensure pieces are the correct colors

### Low Frame Rate
1. Reduce camera resolution in code
2. Close other applications
3. Check CPU usage

### Inaccurate Scoring
1. Ensure pieces are fully visible to camera
2. Check for shadows on pieces
3. Recalibrate colors if needed
4. Verify camera angle provides clear view

## Advanced Customization

### Adjusting Detection Parameters

Edit `tangram_game.py` to modify:
- `PIECE_COLORS`: HSV color ranges
- Minimum contour area (line ~218): `if area < 500:`
- Camera resolution (lines ~210-211)

### Creating New Shapes

Use the shape editor or manually edit `shapes.json`:

```json
{
  "my_shape": {
    "name": "My Custom Shape",
    "difficulty": "medium",
    "pieces": [
      {
        "color": "red",
        "center": [300, 200],
        "angle": 45,
        "piece_type": "large_triangle"
      },
      ...
    ]
  }
}
```

### Scoring Algorithm

The scoring system evaluates:
- **Position accuracy** (60% weight): Distance from target position
- **Angle accuracy** (40% weight): Rotation alignment

Score = Average of all piece scores (0-100%)

## Educational Benefits

This game helps kids develop:
- 🧠 Spatial reasoning
- 🎨 Pattern recognition  
- 🤲 Fine motor skills
- ⏱️ Time management
- 🎯 Problem-solving
- 👁️ Visual perception

## Future Enhancements

Potential additions:
- [ ] Multiple difficulty levels with hints
- [ ] Achievement system and high scores
- [ ] Multiplayer mode (race to complete)
- [ ] More animal shapes
- [ ] Sound effects and music
- [ ] Hint system showing piece placement
- [ ] Tutorial mode for beginners
- [ ] Export/import custom shapes

## License

This project is released under the MIT License. Feel free to modify and distribute.

## Credits

Created for educational purposes to make learning fun through tangram puzzles and computer vision.

---

**Have fun creating and solving tangram puzzles! 🎉**
# tangram
