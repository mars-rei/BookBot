import cv2

path = '/home/takefive/squareblack.jpg'

image = cv2.imread(path)

cv2.namedWindow("Resized_Window", cv2.WINDOW_NORMAL)

cv2.resizeWindow("Resized_Window", 700, 500)

cv2.imshow("Resized_Window", image)
cv2.waitKey(0)