import cv2
import pickle
import cvzone
import numpy as np

# Video feed
cap = cv2.VideoCapture('./Demo/carPark.mp4')

# Load rectangle positions from pickle file
with open('CarParkPos', 'rb') as f:
    rectangles = pickle.load(f)

def checkParkingSpace(img, imgPro):
    free_spaces = 0  # Counter for free spaces
    
    # Iterate through all rectangles and check for occupancy
    for i, rect in enumerate(rectangles):
        (x1, y1), (x2, y2) = rect

        # Draw rectangles on the frame
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 255), 2)

        # Crop the dilated (processed) image within the rectangle area
        imgCrop = imgPro[y1:y2, x1:x2]

        # Count non-zero pixels (indicating occupancy)
        count = cv2.countNonZero(imgCrop)

        # Set color based on occupancy threshold
        if count <900:  # Adjust threshold as needed
            color = (0, 255, 0)  # Green for free
            thickness = 5
            free_spaces += 1  # Increment free space counter
        else:
            color = (0, 0, 255)  # Red for occupied
            thickness = 2

        # Draw updated rectangle color
        cv2.rectangle(img, (x1, y1), (x2, y2), color, thickness)
        
        # Display count inside the rectangle
        #cvzone.putTextRect(img, str(count), (x1, y1 + 20), scale=1, thickness=2, offset=5, colorR=color)

    # Display free/total spaces at the top
    cvzone.putTextRect(img, f'Free: {free_spaces}/{len(rectangles)}', (50, 60), scale=2, thickness=3, offset=10,
                       colorR=(0, 200, 0))

while True:
    # Restart video if it reaches the end
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    success, img = cap.read()
    if not success:
        break

    # Preprocess image for parking space detection
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    # Check and display parking spaces
    checkParkingSpace(img, imgDilate)

    # Display the main frame with rectangles
    cv2.imshow("Video with Rectangles", img)
    # Optional: Display the processed binary image
    cv2.imshow("Processed Image", imgDilate)

    # Press 'q' to quit
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
