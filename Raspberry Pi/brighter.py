import time
import picamera

camera = picamera.PiCamera()
camera.brightness = 60
time.sleep(5)
camera.capture('brighter.jpg')
camera.stop_preview()