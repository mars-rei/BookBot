import picamera
import time

# create a picamera object
camera = picamera.PiCamera()

camera.resolution = (2592, 1944)
camera.framerate = 15
camera.start_preview()
time.sleep(5)
camera.capture('maxRes.jpg')
camera.stop_preview()