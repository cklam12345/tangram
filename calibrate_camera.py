# -*- coding: utf-8 -*-
"""
Camera Calibration Tool
Adjust HSV color ranges for optimal tangram piece detection
"""

import cv2
import numpy as np
import json

# Default HSV ranges
DEFAULT_RANGES = {
    'red': {'lower': [0, 120, 70], 'upper': [10, 255, 255]},
    'blue': {'lower': [100, 120, 70], 'upper': [130, 255, 255]},
    'yellow': {'lower': [20, 120, 70], 'upper': [30, 255, 255]},
    'green': {'lower': [40, 120, 70], 'upper': [80, 255, 255]},
    'orange': {'lower': [10, 120, 70], 'upper': [20, 255, 255]},
    'purple': {'lower': [140, 120, 70], 'upper': [170, 255, 255]},
    'teal': {'lower': [85, 120, 70], 'upper': [95, 255, 255]},
}

class ColorCalibrator:
    """Interactive HSV calibration tool"""
    
    def __init__(self, camera_id=0):
        self.cap = cv2.VideoCapture(camera_id)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        self.current_color = 'red'
        self.colors = list(DEFAULT_RANGES.keys())
        self.ranges = DEFAULT_RANGES.copy()
        
        # Create window and trackbars
        cv2.namedWindow('Calibration')
        cv2.namedWindow('Mask')
        
        self.create_trackbars()
    
    def create_trackbars(self):
        """Create HSV adjustment trackbars"""
        # Hue
        cv2.createTrackbar('H Low', 'Calibration', 
                          self.ranges[self.current_color]['lower'][0], 179, self.on_trackbar)
        cv2.createTrackbar('H High', 'Calibration', 
                          self.ranges[self.current_color]['upper'][0], 179, self.on_trackbar)
        
        # Saturation
        cv2.createTrackbar('S Low', 'Calibration', 
                          self.ranges[self.current_color]['lower'][1], 255, self.on_trackbar)
        cv2.createTrackbar('S High', 'Calibration', 
                          self.ranges[self.current_color]['upper'][1], 255, self.on_trackbar)
        
        # Value
        cv2.createTrackbar('V Low', 'Calibration', 
                          self.ranges[self.current_color]['lower'][2], 255, self.on_trackbar)
        cv2.createTrackbar('V High', 'Calibration', 
                          self.ranges[self.current_color]['upper'][2], 255, self.on_trackbar)
    
    def on_trackbar(self, val):
        """Trackbar callback"""
        pass
    
    def update_trackbars(self):
        """Update trackbar positions for current color"""
        cv2.setTrackbarPos('H Low', 'Calibration', self.ranges[self.current_color]['lower'][0])
        cv2.setTrackbarPos('H High', 'Calibration', self.ranges[self.current_color]['upper'][0])
        cv2.setTrackbarPos('S Low', 'Calibration', self.ranges[self.current_color]['lower'][1])
        cv2.setTrackbarPos('S High', 'Calibration', self.ranges[self.current_color]['upper'][1])
        cv2.setTrackbarPos('V Low', 'Calibration', self.ranges[self.current_color]['lower'][2])
        cv2.setTrackbarPos('V High', 'Calibration', self.ranges[self.current_color]['upper'][2])
    
    def get_current_ranges(self):
        """Get current HSV ranges from trackbars"""
        h_low = cv2.getTrackbarPos('H Low', 'Calibration')
        h_high = cv2.getTrackbarPos('H High', 'Calibration')
        s_low = cv2.getTrackbarPos('S Low', 'Calibration')
        s_high = cv2.getTrackbarPos('S High', 'Calibration')
        v_low = cv2.getTrackbarPos('V Low', 'Calibration')
        v_high = cv2.getTrackbarPos('V High', 'Calibration')
        
        return {
            'lower': [h_low, s_low, v_low],
            'upper': [h_high, s_high, v_high]
        }
    
    def save_ranges(self):
        """Save calibrated ranges to file"""
        with open('color_calibration.json', 'w', encoding='utf-8') as f:
            json.dump(self.ranges, f, indent=2, ensure_ascii=False)
        print("Color ranges saved to color_calibration.json")
    
    def run(self):
        """Main calibration loop"""
        print("Color Calibration Tool")
        print("======================")
        print("Keys:")
        print("  1-7: Switch between colors")
        print("  s: Save calibration")
        print("  r: Reset current color")
        print("  q: Quit")
        print("\nAdjust trackbars to isolate each color piece")
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            # Convert to HSV
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
            # Get current ranges
            current_ranges = self.get_current_ranges()
            self.ranges[self.current_color] = current_ranges
            
            # Create mask
            lower = np.array(current_ranges['lower'])
            upper = np.array(current_ranges['upper'])
            mask = cv2.inRange(hsv, lower, upper)
            
            # Apply morphological operations
            kernel = np.ones((5, 5), np.uint8)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            
            # Find contours
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # Draw contours on original frame
            display_frame = frame.copy()
            cv2.drawContours(display_frame, contours, -1, (0, 255, 0), 2)
            
            # Draw info
            info_text = f"Calibrating: {self.current_color.upper()}"
            cv2.putText(display_frame, info_text, (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            pieces_found = len([c for c in contours if cv2.contourArea(c) > 500])
            count_text = f"Pieces detected: {pieces_found}"
            cv2.putText(display_frame, count_text, (10, 70),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Show frames
            cv2.imshow('Calibration', display_frame)
            cv2.imshow('Mask', mask)
            
            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('q'):
                break
            elif key == ord('s'):
                self.save_ranges()
            elif key == ord('r'):
                self.ranges[self.current_color] = DEFAULT_RANGES[self.current_color].copy()
                self.update_trackbars()
            elif ord('1') <= key <= ord('7'):
                # Switch color
                color_idx = key - ord('1')
                if color_idx < len(self.colors):
                    self.current_color = self.colors[color_idx]
                    self.update_trackbars()
                    print(f"Switched to {self.current_color}")
        
        self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        self.cap.release()
        cv2.destroyAllWindows()


def main():
    calibrator = ColorCalibrator()
    calibrator.run()


if __name__ == "__main__":
    main()
