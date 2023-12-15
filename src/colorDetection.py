import cv2
import numpy as np

#Load an image
image = cv2.imread('your_image.jpg')

#Define the color range you want to detect (for example, green)
lower_range = np.array([0, 100, 0])  # Lower bound for green in BGR
upper_range = np.array([100, 255, 100])  # Upper bound for green in BGR

#Create a mask for the specified color range
mask = cv2.inRange(image, lower_range, upper_range)

#Bitwise AND to extract the detected color
result = cv2.bitwise_and(image, image, mask=mask)

#Show the result
cv2.imshow('Color Detection', result)
cv2.waitKey(0)
cv2.destroyAllWindows()