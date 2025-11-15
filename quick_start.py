"""
Quick Start Script - Test camera and setup
"""

import cv2
import sys

def test_camera():
    """Test if camera is accessible"""
    print("Testing camera access...")
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ ERROR: Could not access camera!")
        print("\nTroubleshooting:")
        print("1. Check if camera is connected")
        print("2. Close other applications using the camera")
        print("3. Check camera permissions")
        return False
    
    print("✓ Camera access OK!")
    
    # Capture a test frame
    ret, frame = cap.read()
    if not ret:
        print("❌ ERROR: Could not read from camera!")
        cap.release()
        return False
    
    print(f"✓ Camera resolution: {frame.shape[1]}x{frame.shape[0]}")
    
    # Show preview
    print("\nShowing camera preview...")
    print("Position your camera to view the desktop")
    print("Press 'q' to continue, 'ESC' to quit")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Draw guide overlay
        h, w = frame.shape[:2]
        cv2.rectangle(frame, (w//4, h//4), (3*w//4, 3*h//4), (0, 255, 0), 2)
        cv2.putText(frame, "Position tangram pieces in this area", 
                   (w//4 + 10, h//4 + 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.putText(frame, "Press 'q' to continue", (10, h - 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        cv2.imshow('Camera Preview', frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == 27:  # ESC
            cap.release()
            cv2.destroyAllWindows()
            return False
    
    cap.release()
    cv2.destroyAllWindows()
    return True

def check_dependencies():
    """Check if required packages are installed"""
    print("Checking dependencies...")
    
    packages = {
        'cv2': 'opencv-python',
        'numpy': 'numpy',
        'pygame': 'pygame'
    }
    
    missing = []
    
    for module, package in packages.items():
        try:
            __import__(module)
            print(f"✓ {package}")
        except ImportError:
            print(f"❌ {package} - MISSING")
            missing.append(package)
    
    if missing:
        print(f"\nPlease install missing packages:")
        print(f"pip install {' '.join(missing)}")
        return False
    
    print("\n✓ All dependencies installed!")
    return True

def main():
    """Main setup check"""
    print("=" * 50)
    print("TANGRAM CHALLENGE - Quick Start Setup")
    print("=" * 50)
    print()
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    print()
    
    # Test camera
    if not test_camera():
        sys.exit(1)
    
    print()
    print("=" * 50)
    print("✓ Setup Complete!")
    print("=" * 50)
    print()
    print("Next steps:")
    print("1. (Optional) Run calibration: python calibrate_camera.py")
    print("2. Start the game: python tangram_game.py")
    print("3. Create shapes: python shape_editor.py")
    print()
    print("Tips for best results:")
    print("- Use bright, solid-colored tangram pieces")
    print("- Ensure good lighting without shadows")
    print("- Use a light-colored desktop surface")
    print("- Position camera 1-2 feet above desktop")
    print()
    print("Have fun! 🎉")

if __name__ == "__main__":
    main()
