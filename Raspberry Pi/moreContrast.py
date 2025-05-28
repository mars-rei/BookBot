import time
import picamera

camera = picamera.PiCamera()

camera.contrast = 75
time.sleep(5)
camera.capture('shapes.jpg')
camera.start_preview()