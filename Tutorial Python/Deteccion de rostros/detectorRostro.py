import cv2
import numpy as numpy

image = cv2.imread('oficina.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

cv2.imshow('image',image)
#cv2.waitkey(0)
cv2.destroyAllWindows()