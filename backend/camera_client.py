import cv2
import requests
from datetime import datetime
import time

API_URL = 'http://localhost:5000/api/attendance'

def mark_attendance(student_id):
    """Mark attendance for a student"""
    now = datetime.now().isoformat()
    payload = {'student_id': student_id, 'in_time': now}
    try:
        r = requests.post(API_URL, json=payload)
        print(f"Attendance marked for student {student_id}: {r.json()}")
    except Exception as e:
        print("Error sending attendance:", e)

def test_camera_access():
    """Test different camera indices to find a working camera"""
    print("Testing camera access...")
    
    # Try different camera indices
    for camera_index in [0, 1, 2]:
        print(f"Trying camera index {camera_index}...")
        cap = cv2.VideoCapture(camera_index)
        
        if cap.isOpened():
            ret, frame = cap.read()
            if ret and frame is not None:
                print(f"Camera {camera_index} is working!")
                cap.release()
                return camera_index
            cap.release()
    
    print("No working camera found!")
    return None

def main():
    print("Starting Camera Client...")
    print("Press 'q' to quit, 'a' to mark attendance manually")
    
    # Test camera access first
    camera_index = test_camera_access()
    if camera_index is None:
        print("\nCamera troubleshooting:")
        print("1. Make sure your camera is connected")
        print("2. Check if another application is using the camera")
        print("3. Try restarting your computer")
        print("4. Check Windows camera privacy settings")
        return
    
    # Try to open camera
    cap = cv2.VideoCapture(camera_index)
    
    if not cap.isOpened():
        print("Error: Could not open camera!")
        return
    
    print(f"Camera {camera_index} opened successfully!")
    print("Camera Client is running...")
    
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            frame_count += 1
            if frame_count > 10:  # Allow some initial frames to fail
                print("Error: Could not read frame from camera!")
                break
            continue
        
        frame_count = 0  # Reset counter on successful frame
        
        # Display the frame
        cv2.imshow('Attendance Camera', frame)
        
        # Handle key presses
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            print("Quitting camera client...")
            break
        elif key == ord('a'):
            # Manual attendance marking
            try:
                student_id = input("Enter student ID: ")
                if student_id.isdigit():
                    mark_attendance(int(student_id))
                else:
                    print("Invalid student ID!")
            except KeyboardInterrupt:
                print("\nCancelled input")
        
        # Small delay to prevent high CPU usage
        time.sleep(0.03)
    
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    print("Camera client stopped.")

if __name__ == "__main__":
    main()
