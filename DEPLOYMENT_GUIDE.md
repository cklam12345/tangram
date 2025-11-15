# Windows Deployment Guide - Tangram Challenge

This guide explains how to create Windows executables for easy deployment and demos.

## 🎯 Goal

Convert Python scripts into standalone Windows applications that:
- Don't require Python installation
- Don't need command line
- Can be launched with double-click
- Look professional for sales demos
- Include a launcher GUI

## 📦 Three Distribution Options

### Option 1: Quick Demo (Recommended for Trade Shows)
**Best for**: Sales demos, trade shows, quick installations  
**Time**: 5 minutes  
**Size**: ~100 MB

### Option 2: Professional Installer
**Best for**: Customer deployments, permanent installations  
**Time**: 15 minutes  
**Size**: ~50 MB (compressed)

### Option 3: Portable Package
**Best for**: USB distribution, no-install demos  
**Time**: 2 minutes  
**Size**: ~100 MB

---

## 🚀 Quick Start - Build Everything

### Automatic Build (Easiest)

**On Windows:**
```batch
# Double-click this file:
build.bat

# Or run in Command Prompt:
build.bat
```

This automatically:
1. Installs PyInstaller
2. Builds all 5 executables
3. Creates portable package
4. Generates installer script

### Manual Build

**If you prefer control:**
```batch
# 1. Install PyInstaller
pip install pyinstaller

# 2. Build executables
python build_windows_exe.py

# 3. Test the launcher
dist\TangramLauncher.exe
```

---

## 📋 Option 1: Quick Demo Package

### What You Get

```
portable_package/
├── TangramLauncher.exe      ← Main launcher (START HERE)
├── TangramGame.exe          ← Game
├── ShapeEditor.exe          ← Editor
├── CameraCalibration.exe    ← Calibration
├── CameraTest.exe           ← Testing
├── README.md                ← Documentation
├── QUICK_REFERENCE.md       ← Commands
└── tangram_icon.ico         ← Icon
```

### How to Use for Demo

1. **Build once:**
   ```batch
   build.bat
   ```

2. **Copy to demo PC:**
   - Copy entire `portable_package` folder to USB drive
   - Or copy to `C:\TangramChallenge\`

3. **Run the demo:**
   - Double-click `TangramLauncher.exe`
   - Click "Play Game" button
   - No installation needed!

4. **For sales team:**
   - Zip the `portable_package` folder
   - Upload to shared drive
   - Sales just unzip and run

### Pros & Cons

✅ **Pros:**
- No installation required
- Works from USB drive
- Perfect for trade shows
- Easy to update (just copy new files)

❌ **Cons:**
- Larger file size (~100 MB)
- No Start Menu integration
- Manual file copying

---

## 📋 Option 2: Professional Installer

### Prerequisites

Download and install [Inno Setup](https://jrsoftware.org/isinfo.php) (free)

### Build Process

1. **Build executables first:**
   ```batch
   build.bat
   ```

2. **Open Inno Setup Compiler**

3. **Load the script:**
   - File → Open
   - Select `tangram_installer.iss`

4. **Compile:**
   - Build → Compile
   - Wait ~1 minute
   - Output: `installer_output\TangramChallenge_Setup.exe`

### What the Installer Does

- Creates Start Menu shortcuts
- Adds desktop icon
- Installs to `C:\Program Files\TangramChallenge\`
- Includes uninstaller
- Looks professional

### Distribution

```batch
# Give customers this ONE file:
TangramChallenge_Setup.exe  (size: ~50 MB)

# They run it, click Next → Next → Install
# Done! Appears in Start Menu
```

### Pros & Cons

✅ **Pros:**
- Professional appearance
- Single file to distribute
- Proper Windows integration
- Uninstaller included
- Smaller download (compressed)

❌ **Cons:**
- Requires Inno Setup to build
- Installation process (not portable)
- Updates need reinstall

---

## 📋 Option 3: Portable ZIP Package

### Quick Creation

```batch
# After building executables:
cd portable_package
# Right-click → Send to → Compressed (zipped) folder

# Or use 7-Zip for better compression:
7z a -tzip TangramChallenge_Portable.zip *
```

### Distribution

1. Upload `TangramChallenge_Portable.zip` to cloud/server
2. Users download and extract
3. Run `TangramLauncher.exe`

---

## 🎨 The Launcher Application

### Features

The launcher provides a **professional GUI** instead of command line:

```
┌────────────────────────────────────┐
│     🎮 Tangram Challenge           │
│  Educational Tangram Puzzle Game   │
├────────────────────────────────────┤
│                                    │
│  [🎮 Play Game]                    │
│  Start the Tangram Challenge!      │
│                                    │
│  [✏️ Shape Editor]                 │
│  Create custom tangram shapes      │
│                                    │
│  [⚙️ Calibrate Camera]             │
│  Adjust color detection settings   │
│                                    │
│  [🔍 Test Camera]                  │
│  Check camera setup                │
│                                    │
│  [📖 Help & Documentation]         │
│                                    │
└────────────────────────────────────┘
```

### Why This is Better for Sales

**Before (Command Line):**
```
Sales: "Now type: python tangram_game.py"
Customer: "What's a Python? Where's the command line?"
Sales: "Let me show you... open PowerShell..."
```

**After (Launcher):**
```
Sales: "Double-click this icon"
Customer: "Oh, easy! [clicks Play Game]"
Sales: "That's it!"
```

---

## 🛠️ Build Details

### What PyInstaller Does

```
Python Script (.py)
        ↓
[PyInstaller Analysis]
        ↓
Bundles:
  • Python interpreter
  • All dependencies (OpenCV, Pygame, NumPy)
  • Your code
  • Required DLLs
        ↓
Single .exe file
```

### Build Options Used

```python
pyinstaller \
  --onefile          # Single executable (not a folder)
  --windowed         # No console window (GUI only)
  --name MyApp       # Custom name
  --icon app.ico     # Custom icon
  --hidden-import    # Include specific modules
```

### File Sizes

| File | Size | Notes |
|------|------|-------|
| TangramLauncher.exe | ~15 MB | Includes tkinter |
| TangramGame.exe | ~80 MB | Includes OpenCV + Pygame |
| ShapeEditor.exe | ~75 MB | Includes Pygame |
| CameraCalibration.exe | ~80 MB | Includes OpenCV |
| CameraTest.exe | ~80 MB | Includes OpenCV |

**Note**: Each .exe includes its own copy of dependencies.  
**Total portable package**: ~330 MB uncompressed

---

## 💼 Sales/Demo Workflow

### For Trade Shows

```mermaid
1. Before Show:
   • Build executables on your PC
   • Copy portable_package to multiple USB drives
   • Test on clean Windows VM

2. At Booth:
   • Plug USB into demo PC
   • Double-click TangramLauncher.exe
   • Click "Test Camera" to verify setup
   • Click "Play Game" to demo

3. For Interested Customers:
   • Give them a USB drive copy
   • Or email them the installer link
   • They can run immediately
```

### For Sales Calls

```
1. Pre-Call:
   • Upload TangramChallenge_Setup.exe to Dropbox/Drive
   • Send customer the download link

2. During Call:
   • Customer downloads installer
   • Runs it while on call with you
   • 2-minute installation
   • Demo live on their machine

3. Follow-Up:
   • Customer can play with it
   • Already installed, no barriers
```

---

## 📊 Comparison Matrix

| Feature | Portable | Installer | Python Scripts |
|---------|----------|-----------|----------------|
| Ease of Use | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ |
| Setup Time | 0 min | 2 min | 10 min |
| Professional Look | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ |
| File Size | Large | Medium | Small |
| Updates | Easy | Reinstall | Easy |
| No Python Needed | ✅ | ✅ | ❌ |
| Start Menu | ❌ | ✅ | ❌ |
| Desktop Icon | Manual | ✅ | ❌ |
| Uninstaller | ❌ | ✅ | ❌ |

**Recommendation**:
- **Trade Shows/Demos**: Portable package
- **Customer Deployments**: Installer
- **Development**: Python scripts

---

## 🔧 Troubleshooting Build Issues

### "PyInstaller not found"

```batch
pip install pyinstaller
```

### "Module not found" errors

Edit `build_windows_exe.py`, add to hidden imports:
```python
cmd.extend([
    "--hidden-import", "your_module",
])
```

### Executables are too large

**Option 1**: Use UPX compression
```batch
pip install pyinstaller[encryption]
pyinstaller --upx-dir=C:\upx ...
```

**Option 2**: Create separate .exe for each
(Already done in our build script)

### Icon doesn't show

1. Install Pillow: `pip install Pillow`
2. Rebuild: `python build_windows_exe.py`
3. Or manually: Create `tangram_icon.ico` (256x256)

---

## 📦 What to Distribute

### Minimum Package (For Demo)

```
TangramChallenge_Demo/
├── TangramLauncher.exe    ← Only this is required!
├── TangramGame.exe
├── ShapeEditor.exe
└── README.txt             ← Basic instructions
```

### Complete Package (For Customers)

```
TangramChallenge_Full/
├── TangramLauncher.exe
├── TangramGame.exe
├── ShapeEditor.exe
├── CameraCalibration.exe
├── CameraTest.exe
├── README.md
├── QUICK_REFERENCE.md
├── SETUP_GUIDE.md
└── example_shapes.json
```

---

## 🚢 Deployment Checklist

### Before Trade Show

- [ ] Build all executables
- [ ] Test on clean Windows PC
- [ ] Create 3+ USB drive copies
- [ ] Print quick reference cards
- [ ] Verify camera compatibility
- [ ] Prepare tangram pieces
- [ ] Test with multiple cameras

### Before Sales Call

- [ ] Upload installer to cloud
- [ ] Test download link
- [ ] Prepare demo script
- [ ] Have backup USB ready
- [ ] Test on customer's Windows version

### For Customer Delivery

- [ ] Build latest version
- [ ] Include all documentation
- [ ] Create installer or portable package
- [ ] Write deployment instructions
- [ ] Include contact information
- [ ] Test uninstall process

---

## 💡 Pro Tips

### Faster Demos

1. **Pre-position camera** before customers arrive
2. **Run Test Camera** once to verify setup
3. **Keep launcher running** between demos
4. **Have backup USB** in case of PC issues

### Better Presentation

1. **Create desktop shortcut** to launcher
2. **Set custom wallpaper** showing tangram pieces
3. **Hide other icons** for clean desktop
4. **Disable sleep mode** on demo PC

### Easier Updates

**For portable version:**
```batch
# Just rebuild and copy new .exe files
python build_windows_exe.py
xcopy /Y dist\*.exe portable_package\
```

**For installer:**
```batch
# Update version in tangram_installer.iss
# Recompile with Inno Setup
```

---

## 🎯 Quick Reference Commands

```batch
# Build everything
build.bat

# Build manually
python build_windows_exe.py

# Test launcher
dist\TangramLauncher.exe

# Create installer (after building)
# Use Inno Setup to compile tangram_installer.iss

# Create portable ZIP
cd portable_package
powershell Compress-Archive * TangramChallenge.zip
```

---

## 📞 Common Questions

**Q: Do customers need Python?**  
A: No! The .exe includes everything.

**Q: Does it work on Windows 11?**  
A: Yes, Windows 7/8/10/11 all supported.

**Q: Can I customize the launcher?**  
A: Yes, edit `launcher.py` and rebuild.

**Q: How do I add my company logo?**  
A: Replace `tangram_icon.ico` and rebuild.

**Q: File size too big?**  
A: Use installer version (compressed) or host on cloud.

**Q: Can I distribute this commercially?**  
A: Yes, MIT license allows commercial use.

---

## 🎉 You're Ready!

**Next Steps:**

1. Run `build.bat`
2. Test `dist\TangramLauncher.exe`
3. Copy to USB or create installer
4. Demo to customers!

**For Help:**
- See `README.md` for game instructions
- See `QUICK_REFERENCE.md` for commands
- See `build_windows_exe.py` for build customization

---

**Your sales team will thank you! No more command line explanations! 🚀**
