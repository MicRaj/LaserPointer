import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while True:
    ret, img = cap.read()
    out_img = img.copy()

    # Convert to BGR
    bgr_img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    # Blur to reduce noise
    bgr_img = cv2.medianBlur(bgr_img, 3)

    # Convert to Lab color space, we only need to check one channel (a-channel) for red
    lab_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2Lab)

    # Threshold the Lab image, keeping only the red pixels
    red_img = cv2.inRange(lab_img, np.array([20, 150, 150]), np.array([190, 255, 255]))

    # Second blur to reduce more noise, easier circle detection
    red_img = cv2.GaussianBlur(red_img, (5, 5), 2, 2)

    # Hough transform to detect circles
    circles = cv2.HoughCircles(red_img, cv2.HOUGH_GRADIENT, 1, red_img.shape[0] / 8, param1=100, param2=18, minRadius=5,
                               maxRadius=500)

    # Draw Rectangle around circles
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        cv2.circle(out_img, center=(circles[0, 0], circles[0, 1]), radius=circles[0, 2], color=(0, 255, 0),
                   thickness=2)
    # Display the resulting frame, quit with q
    cv2.imshow('frame', out_img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()