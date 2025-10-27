import time
import cv2
import imutils
import numpy as np
import pytesseract
from collections import Counter


class DetectVehicle:
    def __init__(self):
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update path
        self.cap = cv2.VideoCapture(0)
        self.plates = []

    def detect_license_plate(self):
        """Detects and extracts the license plate from a USB camera feed."""
        if not self.cap.isOpened():
            print("Error: Could not open camera.")
            return

        time.sleep(2)  # Allow the camera to initialize

        try:
            while len(self.plates) < 5:  # Store five recognized plates
                ret, frame = self.cap.read()
                if not ret:
                    print("Error: Could not read frame.")
                    break

                # Convert to grayscale and apply filtering
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                gray = cv2.bilateralFilter(gray, 11, 17, 17)  # Noise reduction
                edged = cv2.Canny(gray, 50, 150)  # Edge detection

                # Find contours
                cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                cnts = imutils.grab_contours(cnts)
                cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]
                screenCnt = None

                for c in cnts:
                    peri = cv2.arcLength(c, True)
                    approx = cv2.approxPolyDP(c, 0.018 * peri, True)
                    if len(approx) == 4:  # License plates are typically rectangular
                        screenCnt = approx
                        break

                if screenCnt is not None:
                    cv2.drawContours(frame, [screenCnt], -1, (0, 255, 0), 3)

                    # Create a mask for plate extraction
                    mask = np.zeros(gray.shape, np.uint8)
                    cv2.drawContours(mask, [screenCnt], 0, 255, -1)
                    new_image = cv2.bitwise_and(frame, frame, mask=mask)

                    # Crop the license plate region
                    (x, y) = np.where(mask == 255)
                    if x.size == 0 or y.size == 0:
                        print("No license plate region found.")
                        continue  # Skip to next frame

                    (topx, topy) = (np.min(x), np.min(y))
                    (bottomx, bottomy) = (np.max(x), np.max(y))
                    cropped_image = gray[topx:bottomx + 1, topy:bottomy + 1]

                    # Improve OCR accuracy
                    _, cropped_image = cv2.threshold(cropped_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

                    # Extract text using Tesseract OCR
                    try:
                        text = pytesseract.image_to_string(
                            cropped_image,
                            config='--psm 8 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
                        )
                        text = ''.join(filter(str.isalnum, text.strip()))  # Remove unwanted characters

                        if text and len(text) == 6:
                            self.plates.append(text)
                            print("Detected License Plate:", text)
                        else:
                            print("No valid license plate detected.")

                    except Exception as e:
                        print("OCR Error:", e)

                    #cv2.imshow("Cropped License Plate", cropped_image)

                else:
                    print("No license plate contour detected.")

                cv2.imshow("Camera Feed", frame)

                # Exit on 'q' key press
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        finally:
            self.cap.release()  # Ensure camera is released properly
            cv2.destroyAllWindows()

    def plate_number(self):
        """Returns the most frequently detected plate number."""
        self.detect_license_plate()
        print("All detected plates:", self.plates)

        if self.plates:
            numb = max(Counter(self.plates), key=Counter(self.plates).get)
            self.cap.release()  # Ensure camera is released properly
            cv2.destroyAllWindows()
            return numb
        else:
            return "No valid plate detected"


if __name__ == "__main__":

    while True:
        det = DetectVehicle()
        num = det.plate_number()
        print("Final Detected Plate:", num)
        time.sleep(2)  # Small delay before restarting detection
