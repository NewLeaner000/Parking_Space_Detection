import cv2
import pickle

# Initialize global variables
img = cv2.imread('./Img/carParkImg.png')
drawing = False  # True if the mouse is being held down
ix, iy = -1, -1  # Initial point

# Try to load existing rectangles from file, or initialize an empty list
try:
    with open('CarParkPos', 'rb') as f:
        rectangles = pickle.load(f)
except (FileNotFoundError, EOFError):
    rectangles = []  # Initialize to an empty list if file doesn't exist or is empty

# Function to check if a point is inside a rectangle
def point_in_rectangle(point, rect):
    (x1, y1), (x2, y2) = rect
    px, py = point
    return x1 <= px <= x2 and y1 <= py <= y2

# Function to handle mouse events
def draw_rectangle(event, x, y, flags, param):
    global ix, iy, drawing, img, rectangles

    # Start drawing on left mouse button down
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    # Update the rectangle as the mouse moves
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            # Make a copy of the image to show dynamic rectangle
            img_copy = img.copy()
            cv2.rectangle(img_copy, (ix, iy), (x, y), (0, 255, 255), 2)
            cv2.imshow("Image", img_copy)

    # Finalize the rectangle on left mouse button up
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        # Correct coordinates so (x1, y1) is the top-left and (x2, y2) is the bottom-right
        x1, y1 = min(ix, x), min(iy, y)
        x2, y2 = max(ix, x), max(iy, y)
        rectangles.append(((x1, y1), (x2, y2)))
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 255), 2)
        cv2.imshow("Image", img)

    # Delete rectangle on right mouse button down
    elif event == cv2.EVENT_RBUTTONDOWN:
        for rect in rectangles:
            if point_in_rectangle((x, y), rect):
                rectangles.remove(rect)
                img = cv2.imread('./Img/carParkImg.png')  # Reset image
                # Redraw remaining rectangles
                for r in rectangles:
                    cv2.rectangle(img, r[0], r[1], (0, 255, 255), 2)
                cv2.imshow("Image", img)
                break  # Stop after deleting one rectangle

# Load image and set up the mouse callback
if img is None:
    print("Error: Could not read image")
else:
    # Redraw saved rectangles
    for rect in rectangles:
        cv2.rectangle(img, rect[0], rect[1], (0, 255, 255), 2)
    
    cv2.namedWindow("Image")
    cv2.setMouseCallback("Image", draw_rectangle)

    
    while True:
        img_display = img.copy()
        cv2.putText(img_display, "Press 'q' to quit", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.putText(img_display, "Left click to draw", (350, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.putText(img_display, "Right click to delete", (700, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.imshow("Image", img_display)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            # Save rectangles to file on quit
            with open('CarParkPos', 'wb') as f:
                pickle.dump(rectangles, f)
            break

cv2.destroyAllWindows()
