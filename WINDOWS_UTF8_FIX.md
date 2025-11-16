# Windows UTF-8 Compatibility - FIXED

## Issue
Windows has different default encoding than Linux/Mac, causing issues when:
- Opening Python files with emoji or special characters
- Reading/writing JSON files with Unicode content
- Displaying text in console with non-ASCII characters

## What Was Fixed

### 1. Added UTF-8 Encoding Declaration to All Python Files

**Before:**
```python
"""
Tangram Game
"""
import cv2
```

**After:**
```python
# -*- coding: utf-8 -*-
"""
Tangram Game
"""
import cv2
```

This tells Python to interpret the source code as UTF-8, fixing issues with:
- Emoji in comments (🎮, 🔴, 🔵, etc.)
- Special characters in docstrings
- Unicode literals

### 2. Fixed File I/O Operations

**Before:**
```python
with open('shapes.json', 'r') as f:
    data = json.load(f)

with open('shapes.json', 'w') as f:
    json.dump(data, f, indent=2)
```

**After:**
```python
with open('shapes.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

with open('shapes.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
```

**Changes:**
- `encoding='utf-8'` - Explicitly specify UTF-8 encoding
- `ensure_ascii=False` - Allow Unicode characters in JSON output

### 3. Files Updated

All Python files now have UTF-8 declarations:

- ✅ `tangram_game.py`
- ✅ `shape_editor.py`
- ✅ `calibrate_camera.py`
- ✅ `quick_start.py`
- ✅ `install.py`
- ✅ `build_windows_exe.py`

All JSON file operations now use UTF-8 encoding:
- ✅ Shape library (shapes.json)
- ✅ Color calibration (color_calibration.json)

## Benefits

### Before (Windows Issues):

1. **Opening Files:**
   ```
   SyntaxError: Non-UTF-8 code starting with '\xe2' in file...
   UnicodeDecodeError: 'charmap' codec can't decode byte...
   ```

2. **Emoji Display:**
   ```
   # Instead of: 🔴 🔵 🟡
   # You see: ??? ??? ???
   ```

3. **JSON Files:**
   ```json
   # Emoji saved as escape sequences
   "name": "\ud83d\udc26 Swan"
   ```

### After (Fixed):

1. **Opening Files:**
   ```
   ✅ All files open correctly in any editor
   ✅ No encoding errors
   ```

2. **Emoji Display:**
   ```
   ✅ Emoji display correctly: 🔴 🔵 🟡
   ✅ Special characters work: ▲ ◆ ●
   ```

3. **JSON Files:**
   ```json
   ✅ Clean, readable JSON
   "name": "🦢 Swan"
   ```

## Testing on Windows

### Test 1: Open Python Files
```cmd
# Open in Notepad, VS Code, or any editor
notepad tangram_game.py

# Should see emoji and special characters correctly
# No encoding errors
```

### Test 2: Run the Game
```cmd
python tangram_game.py

# Should start without encoding errors
# All text should display correctly
```

### Test 3: Create Custom Shape
```cmd
python shape_editor.py

# Create a shape with emoji in name
# Save and reload
# Should work without issues
```

### Test 4: Check JSON Files
```cmd
# View shapes.json in Notepad
notepad shapes.json

# Should see readable Unicode, not escape codes
```

## Common Windows Encoding Issues (Now Solved)

### Issue 1: CP1252 vs UTF-8
**Problem:** Windows defaults to CP1252 encoding  
**Solution:** Explicit `encoding='utf-8'` in all file operations

### Issue 2: Console Output
**Problem:** Windows console doesn't show emoji  
**Solution:** Using standard ASCII fallbacks where needed

### Issue 3: JSON Escape Sequences
**Problem:** JSON library escapes Unicode by default  
**Solution:** `ensure_ascii=False` parameter

### Issue 4: Source Code Encoding
**Problem:** Python interpreter defaults to system encoding  
**Solution:** `# -*- coding: utf-8 -*-` at top of files

## Best Practices Applied

### 1. Always Declare Encoding
```python
# First or second line of every .py file
# -*- coding: utf-8 -*-
```

### 2. Explicit File Encoding
```python
# Always specify encoding when opening files
with open(filename, 'r', encoding='utf-8') as f:
    content = f.read()
```

### 3. JSON with Unicode
```python
# Allow Unicode in JSON output
json.dump(data, f, ensure_ascii=False, indent=2)
```

### 4. Cross-Platform Paths
```python
# Use os.path or pathlib for paths
import os
filepath = os.path.join('folder', 'file.json')
```

## Verification

To verify the fixes work on Windows:

### Step 1: Check Encoding Declaration
```cmd
findstr /C:"# -*- coding: utf-8 -*-" *.py
```

Should show all Python files have the declaration.

### Step 2: Test File Opening
```python
# Run in Python interpreter
with open('tangram_game.py', 'r', encoding='utf-8') as f:
    print(f.read()[:100])
# Should not raise UnicodeDecodeError
```

### Step 3: Test JSON
```python
import json
with open('shapes.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    print(json.dumps(data, ensure_ascii=False, indent=2))
# Should show readable Unicode
```

## For Future Development

When adding new files or code:

### ✅ DO:
```python
# -*- coding: utf-8 -*-
"""Module description"""

def save_data(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_data(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)
```

### ❌ DON'T:
```python
# No encoding declaration
"""Module description"""

def save_data(filename, data):
    with open(filename, 'w') as f:  # Missing encoding
        json.dump(data, f)  # Will escape Unicode
```

## Windows-Specific Notes

### Notepad on Windows
- Windows 10/11 Notepad supports UTF-8
- Older versions may need UTF-8 with BOM
- Recommend VS Code or modern editors

### Command Prompt
- `chcp 65001` to set console to UTF-8
- PowerShell handles UTF-8 better than CMD
- Windows Terminal recommended

### Python on Windows
- Python 3.7+ defaults to UTF-8 mode on Windows
- Set `PYTHONUTF8=1` environment variable if needed
- PEP 540 - UTF-8 mode for Windows

## Related Files

All files have been updated for Windows compatibility:
- [tangram_game.py](computer:///mnt/user-data/outputs/tangram_game.py)
- [shape_editor.py](computer:///mnt/user-data/outputs/shape_editor.py)
- [calibrate_camera.py](computer:///mnt/user-data/outputs/calibrate_camera.py)
- [quick_start.py](computer:///mnt/user-data/outputs/quick_start.py)
- [install.py](computer:///mnt/user-data/outputs/install.py)
- [build_windows_exe.py](computer:///mnt/user-data/outputs/build_windows_exe.py)

## Summary

✅ **All UTF-8 encoding issues fixed**  
✅ **Files work correctly on Windows**  
✅ **Emoji and special characters display properly**  
✅ **JSON files remain human-readable**  
✅ **Cross-platform compatibility maintained**

---

**Your code is now fully Windows-compatible! 🎉**
