# Tangram Challenge - Quick Reference Card

## Installation (One-time Setup)

```bash
# 1. Install dependencies
python install.py

# 2. Test camera setup
python quick_start.py

# 3. (Optional) Calibrate colors
python calibrate_camera.py
```

## Playing the Game

```bash
python tangram_game.py
```

**Game Controls:**
- `SPACE` - Pause/Resume
- `R` - Reset timer
- `N` - Next shape  
- `ESC` - Quit

**How to Play:**
1. Look at target shape shown on screen
2. Arrange your 7 physical tangram pieces on desktop
3. Try to match the target shape
4. Watch your score increase in real-time!
5. Get 85%+ to complete the challenge

## Creating Custom Shapes

```bash
python shape_editor.py
```

**Editor Controls:**
- `Left Click` - Select/drag pieces
- `Right Click` - Rotate 15°
- `Arrow Keys` - Rotate 5°
- `Delete` - Remove piece
- `C` - Clear all
- `Ctrl+S` - Save shape

**Steps:**
1. Click piece buttons to add to canvas
2. Drag to position, rotate to orient
3. Use all 7 pieces to create shape
4. Save with Ctrl+S
5. Shape appears in game!

## Camera Calibration

```bash
python calibrate_camera.py
```

**Calibration Steps:**
1. Press `1-7` to select color
2. Place piece of that color in view
3. Adjust HSV sliders until piece is isolated
4. Repeat for all 7 colors
5. Press `S` to save
6. Press `Q` to quit

## The 7 Pieces

| Color  | Shape           | Size   |
|--------|-----------------|--------|
| 🔴 Red | Triangle        | Large  |
| 🔵 Blue| Triangle        | Large  |
| 🟢 Green| Triangle       | Medium |
| 🟠 Orange| Parallelogram | Medium |
| 🟡 Yellow| Square        | Medium |
| 🟣 Purple| Triangle      | Small  |
| 🔵 Teal| Triangle        | Small  |

## Default Shapes

| Shape  | Difficulty | Description        |
|--------|------------|--------------------|
| Swan   | Medium     | Water bird         |
| Cat    | Easy       | Sitting cat        |
| Rocket | Hard       | Space rocket       |

## Scoring System

- **85-100%** - ⭐⭐⭐ Excellent! Challenge completed!
- **70-84%**  - ⭐⭐ Great job! Almost there!
- **50-69%**  - ⭐ Good effort! Keep trying!
- **0-49%**   - Keep going! You can do it!

**Score Components:**
- Position accuracy: 60%
- Rotation accuracy: 40%

## Troubleshooting Quick Fixes

| Problem | Solution |
|---------|----------|
| Pieces not detected | Run calibration, improve lighting |
| Wrong colors | Recalibrate specific color |
| Low score despite correct placement | Improve camera angle |
| Game runs slow | Close other apps, reduce camera resolution |
| Camera not found | Check connections, close other camera apps |

## Setup Checklist

- [ ] Python 3.8+ installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Camera positioned 1-2 feet above desktop
- [ ] Good lighting (no shadows)
- [ ] Light-colored desktop surface
- [ ] 7 colored tangram pieces ready
- [ ] Camera tested (`quick_start.py`)
- [ ] Colors calibrated (optional but recommended)

## File Structure

```
tangram_game/
├── tangram_game.py       ← Main game
├── shape_editor.py       ← Create shapes
├── calibrate_camera.py   ← Color tuning
├── quick_start.py        ← Setup test
├── install.py            ← Install script
├── requirements.txt      ← Dependencies
├── shapes.json           ← Shape library (auto-created)
└── README.md             ← Full documentation
```

## Tips for Success

### Camera Setup
✓ Position 1-2 feet above desktop  
✓ Angle slightly downward (30-45°)  
✓ Ensure stable mounting  
✓ Test with `quick_start.py`

### Lighting
✓ Bright, even lighting  
✓ No direct sunlight  
✓ Avoid shadows on pieces  
✓ Multiple light sources best

### Desktop Surface
✓ White or light-colored  
✓ Plain (no patterns)  
✓ Non-reflective  
✓ Clean and clear

### Pieces
✓ Bright, solid colors  
✓ Opaque (not translucent)  
✓ Clean (no dust/dirt)  
✓ Lay flat on surface

## Educational Benefits

This game helps develop:
- 🧠 **Spatial reasoning** - Understanding 2D/3D relationships
- 🎨 **Pattern recognition** - Matching shapes and orientations  
- 🤲 **Fine motor skills** - Precise piece manipulation
- ⏱️ **Time management** - Working under time pressure
- 🎯 **Problem-solving** - Strategic thinking
- 👁️ **Visual perception** - Shape and color discrimination

## Age Recommendations

- **Ages 4-6**: Easy shapes with parental help
- **Ages 7-9**: Medium shapes independently
- **Ages 10+**: Hard shapes, create custom designs

## Common Questions

**Q: Do I need special tangram pieces?**  
A: No! Any colored tangram set works. You can even make your own from cardboard and paint.

**Q: What if I don't have all 7 colors?**  
A: You can modify the PIECE_COLORS in the code to match your available colors.

**Q: Can I play without a camera?**  
A: No, the camera is essential for detecting the physical pieces.

**Q: Will this work on a laptop camera?**  
A: Yes, but you'll need to position the laptop at an angle to view the desktop.

**Q: How do I share my custom shapes?**  
A: Share the `shapes.json` file - others can copy it to their game folder.

## Getting Help

1. Check README.md for detailed instructions
2. Review SETUP_GUIDE.md for piece/camera setup
3. Read ARCHITECTURE.md to understand how it works
4. Run calibration if detection issues persist

## Fun Variations

- **Speed Mode**: How fast can you complete a shape?
- **Memory Challenge**: Look at shape, then build from memory
- **Team Building**: Work together to solve
- **Create & Challenge**: Make shapes for friends to solve
- **Progressive Learning**: Start easy, increase difficulty

---

**Ready to play? Run: `python tangram_game.py`**

Have fun! 🎉
