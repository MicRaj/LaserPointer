import cv2
import serial
import struct


def translate(value, leftMin, leftMax, rightMin, rightMax):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return int(rightMin + (valueScaled * rightSpan))


cap = cv2.VideoCapture(0)
face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
serialCom = serial.Serial('com7', 28800, timeout=.001)

while True:
    ret, img = cap.read()
    out_img = img.copy()

    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    face = face_classifier.detectMultiScale(
        gray_image, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40)
    )

    if face is not None:
        try:
            (xf, yf, w, h) = face[0]
            cv2.rectangle(out_img, (xf, yf), (xf + w, yf + h), (0, 255, 0), 4)
            # Send Coordinates
            x = 180 - translate(xf + w / 2, 0, img.shape[1], 30, 140)
            y = translate(yf + h / 2, 0, img.shape[0], 40, 90)
            serialCom.write(struct.pack('>BB', x, y))
            # Display the resulting frame, quit with q
            cv2.imshow('frame', out_img)
        except:
            print('Face us outside of frame')
            cv2.imshow('frame',img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
