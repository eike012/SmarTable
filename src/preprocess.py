import cv2 
import numpy as np

# Get grayscale image
def getGrayScale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Noise removal
def removeNoise(image):
    return cv2.fastNlMeansDenoising(image, None, 10, 7, 21)

 
# Thresholding
def thresholding(image):
    return cv2.adaptiveThreshold(image,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,2)

# Opening - erosion followed by dilation
def opening(image):
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.erode(image, kernel, iterations=6)
    img = cv2.dilate(image, kernel, iterations=1)
    return img

# Canny edge detection
def canny(image):
    return cv2.Canny(image, 100, 200)

# Skew correction
def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

# Template matching
def matchTemplate(image, template):
    return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
     
# Detect borders of an image 
def detectBorder(imageRead):
    imageRead = getGrayScale(imageRead)
    ret, thresh = cv2.threshold(imageRead,127,255,0)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    area = 0
    for contour in contours:
        if cv2.contourArea(contour) > area:
            finalContour = contour


    cv2.drawContours(imageRead, [finalContour], 0, (0,255,0), 3)
    cv2.imwrite('tests/imageDrawnContour.jpg', imageRead)

# Pre-process image
def preProcess(img):
    image = cv2.imread(img)
    gray = getGrayScale(image)
    denoised = removeNoise(gray)

    cv2.imwrite('images/image.png', denoised)
    return denoised  

