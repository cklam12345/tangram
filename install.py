#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tangram Challenge - Installation Script
Automated setup and dependency installation
"""

import subprocess
import sys
import os

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def check_python_version():
    """Check if Python version is compatible"""
    print("Checking Python version...")
    version = sys.version_info
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python {version.major}.{version.minor} detected")
        print("   Python 3.8 or higher is required")
        return False
    
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
    return True

def install_dependencies():
    """Install required packages"""
    print("\nInstalling dependencies...")
    print("This may take a few minutes...\n")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("\n✓ All dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Installation failed: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    print("\nCreating directories...")
    
    # No special directories needed, but we could add save/config dirs
    print("✓ Directory structure OK")
    return True

def test_imports():
    """Test if all modules can be imported"""
    print("\nTesting imports...")
    
    modules = ['cv2', 'numpy', 'pygame']
    all_ok = True
    
    for module in modules:
        try:
            __import__(module)
            print(f"✓ {module}")
        except ImportError as e:
            print(f"❌ {module} - {e}")
            all_ok = False
    
    return all_ok

def main():
    """Main installation process"""
    print_header("TANGRAM CHALLENGE - INSTALLATION")
    
    # Check Python version
    if not check_python_version():
        print("\nPlease upgrade Python and try again.")
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\nInstallation failed. Please check the errors above.")
        sys.exit(1)
    
    # Create directories
    if not create_directories():
        sys.exit(1)
    
    # Test imports
    if not test_imports():
        print("\n❌ Some modules failed to import.")
        print("Try running: pip install -r requirements.txt")
        sys.exit(1)
    
    # Success!
    print_header("INSTALLATION COMPLETE!")
    
    print("Next steps:")
    print()
    print("1. Setup your camera:")
    print("   python quick_start.py")
    print()
    print("2. (Optional) Calibrate colors:")
    print("   python calibrate_camera.py")
    print()
    print("3. Play the game:")
    print("   python tangram_game.py")
    print()
    print("4. Create custom shapes:")
    print("   python shape_editor.py")
    print()
    print("For detailed instructions, see README.md")
    print()
    print("Have fun! 🎉")

if __name__ == "__main__":
    main()
