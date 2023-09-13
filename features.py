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
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

# Dilation
def dilate(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.dilate(image, kernel, iterations = 1)
    
# Erosion
def erode(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.erode(image, kernel, iterations = 1)

# Opening - erosion followed by dilation
def opening(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

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
    gray = getGrayScale(img)
    cv2.imwrite('tests/gray.png',gray)
    deskewed = deskew(gray)
    cv2.imwrite('tests/deskewed.png',deskewed)
    denoised = removeNoise(deskewed)
    cv2.imwrite('tests/denoised.png',denoised)
    can = canny(denoised)
    cv2.imwrite('tests/canny.png',can)
    thresh = thresholding(denoised)
    cv2.imwrite('tests/thresh.png',thresh)
    dilated = dilate(denoised)
    cv2.imwrite('tests/dilated.png',dilated)
    open = opening(denoised)
    cv2.imwrite('tests/opening.png',open)
    return denoised

# Show boxes of text of image
def showBoxes(img):
    h, w = img.shape
    boxes = pytesseract.image_to_boxes(img) 
    for b in boxes.splitlines():
        b = b.split(' ')
        img = cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)

    cv2.imshow('img', img)
    cv2.waitKey(0)

    # Adding custom options
    custom_config = r'-l por --oem 3 --psm 6'
    img_tes = pytesseract.image_to_string(img, config=custom_config)
    print(img_tes)

    d = pytesseract.image_to_data(img, lang = 'por', output_type=Output.DICT)
    print(d.keys())

img_a = cv2.imread('images/a.jpg')
img_alemao = cv2.imread('images/alemao.jpeg')
img_b = cv2.imread('images/b.jpg')
img_c = cv2.imread('images/c.jpg')

image = preProcess(img_a)
showBoxes(image)
image = preProcess(img_alemao)
showBoxes(image)
image = preProcess(img_b)
showBoxes(image)
image = preProcess(img_c)
showBoxes(image)

img_template = matchTemplate(img_c, img_b)
cv2.imshow('img', img_template)
cv2.waitKey(0)