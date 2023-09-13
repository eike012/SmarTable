import cv2 
import pytesseract
import numpy as np
from pytesseract import Output

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
    img = cv2.erode(image, kernel, iterations=1)
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

# Pre-process image
def preProcess(img):
    img = cv2.GaussianBlur(img, (5, 5), 0)
    gray = getGrayScale(img)
    cv2.imwrite('tests/gray.png',gray)
    deskewed = deskew(gray)
    cv2.imwrite('tests/deskewed.png',deskewed)
    denoised = removeNoise(deskewed)
    cv2.imwrite('tests/denoised.png',denoised)
    open = opening(denoised)
    cv2.imwrite('tests/opening.png',open)
    thresh = thresholding(open)
    cv2.imwrite('tests/thresh.png',thresh)
    can = canny(thresh)
    cv2.imwrite('tests/canny.png',can)
    return thresh

# Show boxes of text of image
def showBoxes(img):
    h, w = img.shape
    boxes = pytesseract.image_to_boxes(img) 
    for b in boxes.splitlines():
        b = b.split(' ')
        img = cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)

    cv2.imshow('img', img)
    cv2.waitKey(0)

# Apply the Tesseract OCR for the provided image
def applyTesseract(img):
    # Adding custom options
    print("\n------------------------------ Applying Tesseract -----------------------------------------\n\n")
    custom_config = r'-l por --oem 1 --psm 5'
    img_tes = pytesseract.image_to_string(img, config=custom_config)
    print(img_tes)

    d = pytesseract.image_to_data(img, lang = 'por', output_type=Output.DICT)

img_a = cv2.imread('images/a.jpg')
img_alemao = cv2.imread('images/alemao.jpeg')
img_b = cv2.imread('images/b.jpg')
img_c = cv2.imread('images/c.jpg')

image = preProcess(img_a)
applyTesseract(image)
#showBoxes(image)
image = preProcess(img_alemao)
applyTesseract(image)
#showBoxes(image)
image = preProcess(img_b)
applyTesseract(image)
#showBoxes(image)
image = preProcess(img_c)
applyTesseract(image)
#showBoxes(image)
