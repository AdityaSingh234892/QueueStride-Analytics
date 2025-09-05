import cv2
import numpy as np

# --- Configuration ---
VIDEO_SOURCE = "C:/Users/Asquare/Downloads/CCTV_Super_Mart_Video_Prompt.mp4" 

# --- Parameters for Automatic Shelf Detection ---
CANNY_LOW_THRESHOLD = 50
CANNY_HIGH_THRESHOLD = 150
HOUGH_THRESHOLD = 50
HOUGH_MIN_LINE_LENGTH = 100
HOUGH_MAX_LINE_GAP = 20
# Define the expected vertical distance between two shelf lines to form a valid ROI
MIN_SHELF_HEIGHT = 80
MAX_SHELF_HEIGHT = 150

# --- Threshold for Emptiness Detection ---
EMPTY_THRESHOLD = 0.55 

def detect_shelf_rois(frame):
    """
    Analyzes a frame to automatically detect shelf locations and returns them as ROIs.
    
    Args:
        frame: The input image/frame.
        
    Returns:
        A list of tuples, where each tuple is an ROI in (x, y, w, h) format.
    """
    # Convert frame to grayscale, blur, and detect edges
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, CANNY_LOW_THRESHOLD, CANNY_HIGH_THRESHOLD)

    # Detect lines using Hough Line Transform
    lines = cv2.HoughLinesP(
        edges, 1, np.pi / 180, HOUGH_THRESHOLD,
        minLineLength=HOUGH_MIN_LINE_LENGTH, maxLineGap=HOUGH_MAX_LINE_GAP
    )

    if lines is None:
        return []

    # Filter for horizontal lines and sort them by their y-coordinate
    horizontal_lines = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        angle = np.abs(np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi)
        if angle < 10 or angle > 170:
            horizontal_lines.append(line[0])
            
    horizontal_lines.sort(key=lambda line: line[1])

    # Group lines to form shelf ROIs
    shelf_rois = []
    i = 0
    while i < len(horizontal_lines) - 1:
        y1 = horizontal_lines[i][1]
        j = i + 1
        while j < len(horizontal_lines):
            y2 = horizontal_lines[j][1]
            height = y2 - y1
            if MIN_SHELF_HEIGHT <= height <= MAX_SHELF_HEIGHT:
                # Found a pair of lines that form a shelf
                x1_top, _, x2_top, _ = horizontal_lines[i]
                x1_bot, _, x2_bot, _ = horizontal_lines[j]
                
                # Define the ROI
                x = int(min(x1_top, x1_bot))
                w = int(max(x2_top, x2_bot) - x)
                
                # Add a small padding and ensure ROI is within frame bounds
                y = y1 + 5 
                h = height - 10
                if w > 0 and h > 0:
                    shelf_rois.append((x, y, w, h))
                i = j -1 # Move to the line after the bottom of the current shelf
                break
            j += 1
        i += 1
        
    return shelf_rois


def main():
    """
    Main function to run the fully automated shelf monitoring application.
    """
    cap = cv2.VideoCapture(VIDEO_SOURCE)
    if not cap.isOpened():
        print(f"Error: Could not open video source: {VIDEO_SOURCE}")
        return

    # 1. Get the first frame for reference and shelf detection
    ret, reference_frame = cap.read()
    if not ret:
        print("Error: Could not read the first frame.")
        cap.release()
        return

    # 2. Automatically detect shelf ROIs from the first frame
    print("Detecting shelves automatically...")
    shelf_rois = detect_shelf_rois(reference_frame)
    if not shelf_rois:
        print("Could not automatically detect any shelves. Exiting.")
        print("Try adjusting the Canny or Hough parameters.")
        cap.release()
        return
    print(f"Successfully detected {len(shelf_rois)} shelf regions to monitor.")

    # 3. Prepare reference images for each detected ROI
    reference_gray = cv2.cvtColor(reference_frame, cv2.COLOR_BGR2GRAY)
    reference_rois_data = [reference_gray[y:y+h, x:x+w] for x, y, w, h in shelf_rois]

    # 4. Process the rest of the video
    while True:
        ret, frame = cap.read()
        if not ret:
            print("End of video.")
            break

        output_frame = frame.copy()
        current_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 5. Analyze each automatically detected ROI
        for i, (x, y, w, h) in enumerate(shelf_rois):
            # Ensure ROI dimensions are valid before slicing
            if w <= 0 or h <= 0:
                continue

            current_roi = current_gray[y:y+h, x:x+w]
            ref_roi = reference_rois_data[i]
            
            # Resize for consistent comparison if needed (optional, but good practice)
            if current_roi.shape != ref_roi.shape:
                ref_roi = cv2.resize(ref_roi, (current_roi.shape[1], current_roi.shape[0]))

            # --- Emptiness Detection Logic ---
            diff = cv2.absdiff(ref_roi, current_roi)
            _, thresholded_diff = cv2.threshold(diff, 50, 255, cv2.THRESH_BINARY)
            
            non_zero_count = cv2.countNonZero(thresholded_diff)
            total_pixels = w * h
            change_percentage = non_zero_count / total_pixels if total_pixels > 0 else 0

            # --- Visualization and Alerting ---
            if change_percentage > EMPTY_THRESHOLD:
                color = (0, 0, 255)  # Red for ALERT
                status_text = f"ALERT: REFILL ({change_percentage:.2%})"
                thickness = 2
            else:
                color = (0, 255, 0)  # Green for OK
                status_text = f"OK ({change_percentage:.2%})"
                thickness = 1

            cv2.rectangle(output_frame, (x, y), (x + w, y + h), color, thickness)
            cv2.putText(output_frame, status_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        cv2.imshow('Automated Stock Monitoring AI', output_frame)

        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("Monitoring stopped.")

if __name__ == "__main__":
    main()
