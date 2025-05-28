#!/usr/bin/env python3
import serial     

import cv2
import numpy as np
import time
import imutils

# Use the default camera device ID (usually 0 for the built-in webcam)
CAMERA_DEVICE_ID = 0
IMAGE_WIDTH = 320
IMAGE_HEIGHT = 240
fps = 0

def set_camera_properties(cap, width, height):
    cap.set(3, width)
    cap.set(4, height)

def capture_frame(cap):
    ret, frame = cap.read()
    if not ret:
        raise ValueError("Failed to read a frame from the camera")
    return frame

def visualize_fps(image, fps: float) -> np.ndarray:
    if len(np.shape(image)) < 3:
        text_color = (255, 255, 255)
    else:
        text_color = (0, 255, 0)
    
    row_size = 20
    left_margin = 24
    font_size = 1
    font_thickness = 1
    
    fps_text = 'FPS: {:.1f}'.format(fps)
    text_location = (left_margin, row_size)
    cv2.putText(image, fps_text, text_location, cv2.FONT_HERSHEY_PLAIN,
                font_size, text_color, font_thickness)
 
    return image

class ShapeDetector:
    def _init_(self):
        pass
    def detect(self, c):
        shape = "unidentified"
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * peri, True)
        if len(approx) == 3:
            shape = "triangle"
            #print('traingle found')
        elif len(approx) == 4:
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)
            if ar >= 0.95 and ar <= 1.05:
                shape = "square"
                #print('square found')
            else:
                shape = "rectangle"
                #print('rectangle found')
        elif len(approx) == 5:
            shape = "pentagon"
            #print('pentagon found')
        elif len(approx) == 6:
            shape = "hexagon"
            #print('hexagon found')
        elif len(approx) == 10 or len(approx) == 12:
            shape = "star"
            #print('star found')
        else:
            shape = "circle"
            #print('circle found')
        
        return shape

def main():
    
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=100)
    ser.reset_input_buffer()
    
    try:
        cap = cv2.VideoCapture(CAMERA_DEVICE_ID)
        if not cap.isOpened():
            raise ValueError("Could not open the camera")
        set_camera_properties(cap, IMAGE_WIDTH, IMAGE_HEIGHT)
 
        print("Press 'Esc' to exit...")
        
        fps = 0
 
        while True:
                        
            start_time = time.time()
            
            frame = capture_frame(cap)
            
            resized = imutils.resize(frame, width=300)
            ratio = frame.shape[0] / float(resized.shape[0])
            
            gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]
            
            cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            sd = ShapeDetector()
            
            for c in cnts:
                M = cv2.moments(c)
                if M["m00"] != 0:
                    cX = int((M["m10"] / M["m00"]) * ratio)
                    cY = int((M["m01"] / M["m00"]) * ratio)  
                    
                    shape = sd.detect(c)
                    
                    c = c.astype("float")
                    c *= ratio
                    c = c.astype("int")
                    cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)
                    
                    mask = np.zeros(frame.shape[:2], np.uint8)
                    cv2.drawContours(mask, [c], -1, 255, -1)
                    
                    mean_color_bgr = cv2.mean(frame, mask=mask)[:3]
                    mean_color_hsv = cv2.cvtColor(np.uint8([[mean_color_bgr]]), cv2.COLOR_BGR2HSV)[0][0]
                    
                    if (0 <= mean_color_hsv[0] <= 10) or (170 <= mean_color_hsv[0] <= 180):
                        shapeColour = 'red'
                    elif 100 <= mean_color_hsv[0] <= 130:
                        shapeColour = 'blue'
                    elif 20 <= mean_color_hsv[0] <= 30:
                        shapeColour = 'yellow'
                    else:
                        shapeColour = 'unidentified'
                    
                    mean2 = (255 - mean_color_bgr[0], 255 - mean_color_bgr[1], 255 - mean_color_bgr[2])
                    mean2 = (int(mean2[0]), int(mean2[1]), int(mean2[2]))
                    
                    if shape != 'unidentified' and shape != 'hexagon' and shape != 'star':
                        if shapeColour != 'unidentified':
                            objLbl = shape + " {}".format(shapeColour)
                        else:
                            objLbl = shape
                            
                        textSize = cv2.getTextSize(objLbl, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)[0]

                        if shape == "circle" and shapeColour == "yellow":
                            message = "Computer Science"
                            ser.write(b"Computer Science\n")
                        elif shape == "square" and shapeColour == "blue":
                            message = "Marketing"
                            ser.write(b"Marketing\n")
                        elif shape == "triangle" and shapeColour == "red":
                            message = "Business"
                            ser.write(b"Business\n")
                        else:
                            message = None
                        
                        if message:
                            cv2.putText(frame, message, (int(cX - textSize[0] / 2), int(cY + textSize[1] / 2)), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255), 1)
 
            end_time = time.time()
            seconds = end_time - start_time
            fps = 1.0 / seconds
 
            cv2.imshow("Shape Detection", visualize_fps(frame, fps))
 
            if cv2.waitKey(33) == 27:  # Escape key
                break
 
    except Exception as e:
        print(e)
 
    finally:
        cv2.destroyAllWindows()
        cap.release()
 
if __name__ == "__main__":
    main()

