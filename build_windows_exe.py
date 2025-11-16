# -*- coding: utf-8 -*-
"""
Build Windows Executable
Creates standalone .exe files for easy deployment
"""

import subprocess
import sys
import os

def check_pyinstaller():
    """Check if PyInstaller is installed"""
    try:
        import PyInstaller
        print("✓ PyInstaller is installed")
        return True
    except ImportError:
        print("Installing PyInstaller...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("✓ PyInstaller installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install PyInstaller")
            return False

def build_executable(script_name, exe_name, icon_path=None):
    """Build a single executable"""
    print(f"\nBuilding {exe_name}...")
    
    cmd = [
        "pyinstaller",
        "--onefile",  # Single executable
        "--windowed",  # No console window for GUI apps
        "--name", exe_name,
        "--clean",
    ]
    
    if icon_path and os.path.exists(icon_path):
        cmd.extend(["--icon", icon_path])
    
    # Add hidden imports for pygame and opencv
    cmd.extend([
        "--hidden-import", "pygame",
        "--hidden-import", "cv2",
        "--hidden-import", "numpy",
    ])
    
    cmd.append(script_name)
    
    try:
        subprocess.check_call(cmd)
        print(f"✓ {exe_name}.exe created successfully")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Failed to build {exe_name}")
        return False

def create_launcher():
    """Create a simple launcher GUI"""
    launcher_code = '''"""
Tangram Challenge Launcher
Simple GUI to launch game components
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
import sys

class TangramLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("Tangram Challenge")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        
        # Set icon if available
        try:
            self.root.iconbitmap("tangram_icon.ico")
        except:
            pass
        
        # Header
        header = tk.Label(
            root, 
            text="🎮 Tangram Challenge",
            font=("Arial", 24, "bold"),
            fg="#2E86AB"
        )
        header.pack(pady=20)
        
        subtitle = tk.Label(
            root,
            text="Educational Tangram Puzzle Game",
            font=("Arial", 12),
            fg="#666"
        )
        subtitle.pack(pady=5)
        
        # Separator
        ttk.Separator(root, orient="horizontal").pack(fill="x", padx=20, pady=20)
        
        # Button frame
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10, fill="both", expand=True, padx=40)
        
        # Buttons
        self.create_button(
            button_frame,
            "🎮 Play Game",
            "Start the Tangram Challenge game!",
            self.launch_game,
            "#4CAF50"
        )
        
        self.create_button(
            button_frame,
            "✏️ Shape Editor",
            "Create custom tangram shapes",
            self.launch_editor,
            "#2196F3"
        )
        
        self.create_button(
            button_frame,
            "⚙️ Calibrate Camera",
            "Adjust color detection settings",
            self.launch_calibrate,
            "#FF9800"
        )
        
        self.create_button(
            button_frame,
            "🔍 Test Camera",
            "Check camera setup and positioning",
            self.launch_test,
            "#9C27B0"
        )
        
        # Separator
        ttk.Separator(root, orient="horizontal").pack(fill="x", padx=20, pady=20)
        
        # Help button
        help_btn = tk.Button(
            root,
            text="📖 Help & Documentation",
            command=self.show_help,
            font=("Arial", 11),
            bg="#E0E0E0",
            fg="#333",
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=10
        )
        help_btn.pack(pady=10)
        
        # Footer
        footer = tk.Label(
            root,
            text="Version 1.0 | Made with ❤️ for Education",
            font=("Arial", 9),
            fg="#999"
        )
        footer.pack(side="bottom", pady=10)
    
    def create_button(self, parent, text, description, command, color):
        """Create a styled button with description"""
        frame = tk.Frame(parent, bg="white", relief="solid", borderwidth=1)
        frame.pack(pady=10, fill="x")
        
        btn = tk.Button(
            frame,
            text=text,
            command=command,
            font=("Arial", 14, "bold"),
            bg=color,
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=15
        )
        btn.pack(fill="x")
        
        desc = tk.Label(
            frame,
            text=description,
            font=("Arial", 9),
            fg="#666",
            bg="white"
        )
        desc.pack(pady=(5, 10))
    
    def launch_game(self):
        """Launch the main game"""
        self.run_executable("TangramGame.exe", "tangram_game.py")
    
    def launch_editor(self):
        """Launch the shape editor"""
        self.run_executable("ShapeEditor.exe", "shape_editor.py")
    
    def launch_calibrate(self):
        """Launch camera calibration"""
        self.run_executable("CameraCalibration.exe", "calibrate_camera.py")
    
    def launch_test(self):
        """Launch camera test"""
        self.run_executable("CameraTest.exe", "quick_start.py")
    
    def run_executable(self, exe_name, fallback_script):
        """Run executable or fallback to Python script"""
        try:
            # Try to run .exe
            if os.path.exists(exe_name):
                subprocess.Popen([exe_name])
            # Try from dist folder
            elif os.path.exists(os.path.join("dist", exe_name)):
                subprocess.Popen([os.path.join("dist", exe_name)])
            # Fallback to Python script
            elif os.path.exists(fallback_script):
                subprocess.Popen([sys.executable, fallback_script])
            else:
                messagebox.showerror(
                    "Error",
                    f"Could not find {exe_name} or {fallback_script}\\n\\n"
                    "Please ensure the files are in the same directory."
                )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch: {str(e)}")
    
    def show_help(self):
        """Show help dialog"""
        help_text = """
🎮 TANGRAM CHALLENGE - Quick Help

GETTING STARTED:
1. Click "Test Camera" to check your setup
2. (Optional) Use "Calibrate Camera" to tune colors
3. Click "Play Game" to start!

REQUIREMENTS:
• PC camera positioned above desktop
• 7 colored tangram pieces (see guide)
• Good lighting without shadows
• Light-colored desktop surface

GAME CONTROLS:
• SPACE - Pause/Resume
• R - Reset timer
• N - Next shape
• ESC - Quit

For detailed instructions, see:
README.md or QUICK_REFERENCE.md

Enjoy! 🎉
        """
        
        messagebox.showinfo("Help", help_text)

def main():
    root = tk.Tk()
    app = TangramLauncher(root)
    root.mainloop()

if __name__ == "__main__":
    main()
'''
    
    with open("launcher.py", "w") as f:
        f.write(launcher_code)
    
    print("✓ Launcher script created")

def create_icon():
    """Create a simple icon for the application"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # Create a simple icon
        img = Image.new('RGB', (256, 256), color='#2E86AB')
        draw = ImageDraw.Draw(img)
        
        # Draw tangram-like shapes
        # Triangle 1
        draw.polygon([(50, 50), (128, 50), (128, 128)], fill='#FF6B6B')
        # Triangle 2
        draw.polygon([(128, 50), (206, 50), (128, 128)], fill='#4ECDC4')
        # Square
        draw.polygon([(128, 128), (206, 128), (206, 206), (128, 206)], fill='#FFE66D')
        # Triangle 3
        draw.polygon([(50, 128), (128, 128), (128, 206)], fill='#95E1D3')
        
        img.save("tangram_icon.png", "PNG")
        
        # Try to convert to ICO
        try:
            img.save("tangram_icon.ico", format="ICO", sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
            print("✓ Icon created: tangram_icon.ico")
            return "tangram_icon.ico"
        except:
            print("✓ Icon created: tangram_icon.png (install Pillow for .ico)")
            return None
            
    except ImportError:
        print("⚠ Pillow not installed, skipping icon creation")
        print("  Install with: pip install Pillow")
        return None

def create_installer_script():
    """Create an Inno Setup script for Windows installer"""
    inno_script = """
; Tangram Challenge Installer Script
; Requires Inno Setup: https://jrsoftware.org/isinfo.php

[Setup]
AppName=Tangram Challenge
AppVersion=1.0
DefaultDirName={autopf}\\TangramChallenge
DefaultGroupName=Tangram Challenge
OutputDir=installer_output
OutputBaseFilename=TangramChallenge_Setup
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
SetupIconFile=tangram_icon.ico

[Files]
Source: "dist\\TangramLauncher.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\\TangramGame.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\\ShapeEditor.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\\CameraCalibration.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\\CameraTest.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "QUICK_REFERENCE.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "shapes.json"; DestDir: "{app}"; Flags: ignoreversion onlyifdoesntexist
Source: "tangram_icon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\\Tangram Challenge"; Filename: "{app}\\TangramLauncher.exe"
Name: "{autodesktop}\\Tangram Challenge"; Filename: "{app}\\TangramLauncher.exe"
Name: "{group}\\Play Game"; Filename: "{app}\\TangramGame.exe"
Name: "{group}\\Shape Editor"; Filename: "{app}\\ShapeEditor.exe"
Name: "{group}\\Uninstall"; Filename: "{uninstallexe}"

[Run]
Filename: "{app}\\TangramLauncher.exe"; Description: "Launch Tangram Challenge"; Flags: nowait postinstall skipifsilent
"""
    
    with open("tangram_installer.iss", "w") as f:
        f.write(inno_script)
    
    print("✓ Inno Setup script created: tangram_installer.iss")
    print("  Download Inno Setup from: https://jrsoftware.org/isinfo.php")

def main():
    print("=" * 60)
    print("  TANGRAM CHALLENGE - WINDOWS EXECUTABLE BUILDER")
    print("=" * 60)
    print()
    
    # Check PyInstaller
    if not check_pyinstaller():
        return
    
    # Create launcher
    print("\nCreating launcher...")
    create_launcher()
    
    # Create icon
    print("\nCreating icon...")
    icon_path = create_icon()
    
    # Build executables
    print("\n" + "=" * 60)
    print("  BUILDING EXECUTABLES")
    print("=" * 60)
    
    apps = [
        ("launcher.py", "TangramLauncher", icon_path),
        ("tangram_game.py", "TangramGame", icon_path),
        ("shape_editor.py", "ShapeEditor", icon_path),
        ("calibrate_camera.py", "CameraCalibration", icon_path),
        ("quick_start.py", "CameraTest", icon_path),
    ]
    
    success_count = 0
    for script, name, icon in apps:
        if os.path.exists(script):
            if build_executable(script, name, icon):
                success_count += 1
        else:
            print(f"⚠ Skipping {script} - file not found")
    
    # Create installer script
    print("\n" + "=" * 60)
    print("  CREATING INSTALLER SCRIPT")
    print("=" * 60)
    create_installer_script()
    
    # Summary
    print("\n" + "=" * 60)
    print("  BUILD COMPLETE!")
    print("=" * 60)
    print(f"\n✓ Successfully built {success_count} executables")
    print("\nExecutables are in the 'dist' folder:")
    print("  • TangramLauncher.exe - Main launcher (START HERE)")
    print("  • TangramGame.exe - Game application")
    print("  • ShapeEditor.exe - Shape creation tool")
    print("  • CameraCalibration.exe - Color calibration")
    print("  • CameraTest.exe - Camera testing")
    
    print("\nNEXT STEPS:")
    print("\n1. For quick demo:")
    print("   → Just run: dist\\TangramLauncher.exe")
    
    print("\n2. For professional installer:")
    print("   → Download Inno Setup: https://jrsoftware.org/isinfo.php")
    print("   → Compile: tangram_installer.iss")
    print("   → Creates: TangramChallenge_Setup.exe")
    
    print("\n3. For portable package:")
    print("   → Copy entire 'dist' folder")
    print("   → Include: README.md, QUICK_REFERENCE.md")
    print("   → Zip and share!")
    
    print("\n" + "=" * 60)
    print("Ready for demo! 🎉")
    print("=" * 60)

if __name__ == "__main__":
    main()
