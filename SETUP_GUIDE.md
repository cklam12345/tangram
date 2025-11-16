# Tangram Piece Setup Guide

## Physical Piece Requirements

### The 7 Tangram Pieces

Your tangram set should include these 7 pieces in the specified colors:

```
┌─────────────────────────────────────────────────────────────┐
│                    TANGRAM PIECES                            │
└─────────────────────────────────────────────────────────────┘

1. RED - Large Triangle (Big)
   
        ▲
       ████
      ██████
     ████████
    ██████████

2. BLUE - Large Triangle (Big)
   
        ▲
       ████
      ██████
     ████████
    ██████████

3. GREEN - Medium Triangle (Medium)
   
       ▲
      ████
     ██████
    ████████

4. ORANGE - Parallelogram (Medium)
   
    ████████
      ████████
        ████████

5. YELLOW - Square
   
    ████████
    ████████
    ████████
    ████████

6. PURPLE - Small Triangle (Small)
   
      ▲
     ████
    ██████

7. TEAL/CYAN - Small Triangle (Small)
   
      ▲
     ████
    ██████
```

## Piece Specifications

### Size Ratios (Approximate)
- Large Triangles (2): 100% (base size)
- Medium Triangle (1): 70% of large
- Small Triangles (2): 50% of large
- Square (1): 70% of large
- Parallelogram (1): 70% of large

### Color Requirements

**Must Have:**
- Solid, opaque colors (not translucent)
- Bright, saturated colors
- Matte or semi-gloss finish (not highly reflective)
- Consistent color throughout piece

**Color Palette:**

```
🔴 RED        RGB(255, 0, 0)     Bright red, like a fire truck
🔵 BLUE       RGB(0, 0, 255)     Primary blue, like sky
🟡 YELLOW     RGB(255, 255, 0)   Bright yellow, like sun
🟢 GREEN      RGB(0, 255, 0)     Bright green, like grass
🟠 ORANGE     RGB(255, 165, 0)   Orange, like traffic cone
🟣 PURPLE     RGB(255, 0, 255)   Magenta/purple
🔵 TEAL       RGB(0, 255, 255)   Cyan/teal, like ocean
```

## Where to Get Tangram Pieces

### Option 1: Purchase Ready-Made Set
- Search "tangram puzzle set" on Amazon/eBay
- Look for foam or wooden pieces
- Ensure bright colors
- Cost: $5-15

### Option 2: Make Your Own (DIY)

**Materials:**
- Colored foam sheets (craft store)
- Colored cardstock/cardboard
- Construction paper (laminated)

**Steps:**
1. Print tangram template
2. Cut out shapes
3. Trace onto colored materials
4. Cut carefully
5. (Optional) Laminate for durability

### Option 3: 3D Print
- Download STL files online
- Print in different colored filaments
- Recommended thickness: 3-5mm

### Option 4: Paint Wooden Pieces
- Buy unpainted tangram set
- Paint with bright acrylic colors
- Let dry completely
- Apply clear coat for protection

## Camera Setup

### Ideal Setup

```
     [Camera]        ← Position 1-2 feet above desktop
        │
        │ 45° angle (adjustable)
        │
        ▼
   ┌─────────────────┐
   │                 │ ← Light colored desktop surface
   │  Tangram Area   │    (white, light gray, beige)
   │                 │
   │    [Pieces]     │ ← Place pieces here
   │                 │
   └─────────────────┘
```

### Lighting Recommendations

```
┌──[Light Source]──┐
│                  │
│   Even, diffuse  │ ← Avoid direct spotlight
│     lighting     │
│                  │
└──────────────────┘
         │
         ▼
    [Desktop]

✓ Good:
  - Overhead room lighting
  - Natural daylight (indirect)
  - Multiple light sources
  - LED panels (diffused)

✗ Avoid:
  - Direct sunlight
  - Single spotlight
  - Shadows on pieces
  - Colored lighting
```

## Desktop Surface

### Best Surfaces

```
✓ Excellent:
  • White poster board
  • Light gray mat
  • Beige/tan table
  • White tablecloth

✓ Good:
  • Light wood finish
  • Plain white paper
  • Neutral colors

✗ Avoid:
  • Dark surfaces (black, dark brown)
  • Patterned surfaces
  • Reflective surfaces (glass, metal)
  • Colored surfaces that match pieces
```

## Testing Your Setup

### Quick Test Checklist

1. **Camera Test**
   ```
   Run: python quick_start.py
   
   Check:
   □ Camera preview shows clear image
   □ Desktop area is visible
   □ Lighting is even
   □ No shadows or glare
   ```

2. **Color Detection Test**
   ```
   Run: python calibrate_camera.py
   
   For each color:
   □ Place piece in view
   □ Adjust HSV sliders
   □ Piece is clearly detected (white mask)
   □ Little to no background noise
   □ Save calibration
   ```

3. **Game Test**
   ```
   Run: python tangram_game.py
   
   Check:
   □ All 7 pieces detected
   □ Pieces display correctly
   □ Score changes when moving pieces
   □ Rotation is detected
   ```

## Troubleshooting

### Pieces Not Detected

**Problem**: Piece doesn't appear on screen

**Solutions**:
1. Improve lighting (brighter, more even)
2. Use lighter desktop surface
3. Recalibrate color (calibrate_camera.py)
4. Check piece color matches expected color
5. Ensure piece is fully visible to camera

### Wrong Color Detected

**Problem**: Red piece detected as orange

**Solutions**:
1. Adjust HSV ranges in calibration
2. Increase lighting
3. Check for color bleed/reflection
4. Use more saturated piece color

### Multiple Detections

**Problem**: One piece shows multiple times

**Solutions**:
1. Reduce sensitivity in calibration
2. Remove shadows
3. Avoid reflective surfaces
4. Check for colored objects nearby

### Poor Accuracy

**Problem**: Score doesn't match actual arrangement

**Solutions**:
1. Improve camera angle (more overhead)
2. Better lighting (reduce shadows)
3. Recalibrate all colors
4. Check camera focus
5. Ensure pieces lay flat

## Advanced Tips

### Professional Setup

For best results:

1. **Camera Mount**
   - Use tripod or fixed mount
   - Minimize vibration
   - Adjustable angle

2. **Lighting Rig**
   - Two LED panels at 45° angles
   - Diffusers to soften light
   - Adjustable brightness

3. **Play Surface**
   - White foam board (20" x 20")
   - Non-reflective finish
   - Marked play area

4. **Piece Storage**
   - Labeled containers
   - Keep pieces clean
   - Avoid scratches/damage

### Creating Perfect Pieces

**Ideal Piece Properties**:
- Thickness: 3-5mm
- Edge quality: Smooth, clean cuts
- Surface: Matte finish
- Color: Uniform throughout
- Shape: Precise angles

**Coating Options**:
- Clear acrylic spray (matte)
- Lamination
- Mod Podge (matte)

### Color Consistency

**Tip**: Use color swatches to verify

1. Print color reference chart
2. Compare physical pieces
3. Adjust under camera lighting
4. Calibrate accordingly

## Classroom/Group Setup

### Multiple Stations

```
Station 1     Station 2     Station 3
[Camera]      [Camera]      [Camera]
   │             │             │
   ▼             ▼             ▼
[Desk 1]      [Desk 2]      [Desk 3]

Each station needs:
- PC with game installed
- Camera mount
- Lighting
- Tangram set
- Light surface
```

### Group Activity Ideas

1. **Race Mode**
   - Multiple kids, one shape
   - First to 85% wins
   - Team collaboration

2. **Creative Challenge**
   - Kids create shapes
   - Others try to replicate
   - Vote on best design

3. **Progressive Difficulty**
   - Start with easy shapes
   - Unlock harder shapes
   - Achievement tracking

---

**Remember**: The key to success is good lighting, proper camera positioning, and accurately colored pieces!
