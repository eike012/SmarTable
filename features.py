import cv2 
import pytesseract
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import easyocr

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
    gray = getGrayScale(img)
    cv2.imwrite('tests/gray.png',gray)
    # gray = cv2.rotate(gray, cv2.ROTATE_90_CLOCKWISE)
    deskewed = gray
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
def showBoxes(img, bounds, color="yellow", width=2):
    image = Image.open(img)
    draw = ImageDraw.Draw(image)
    for bound in bounds:
        p0, p1, p2 , p3 = bound[0]
        draw.line([*p0, *p1, *p2, *p3, *p0], fill=color, width=width)
    
    image.show()

def processImageWithEasyOCR(img):
    # Initialize EasyOCR reader
    reader = easyocr.Reader(['pt'])

    # Process the entire image using EasyOCR
    results = reader.readtext(img)

    # Print EasyOCR results for the entire image
    for (bbox, text, prob) in results:
        print(text)
    
    return results

img_a = 'images/a.jpg'
img_alemao = 'images/alemao.jpeg'
img_b = 'images/b.jpg'
img_c = 'images/c.jpg'


# image = preProcess(img_a)
results = processImageWithEasyOCR(img_a)
showBoxes(img_a, results)
results = processImageWithEasyOCR(img_alemao)
showBoxes(img_alemao, results)
results = processImageWithEasyOCR(img_b)
showBoxes(img_b, results)
results = processImageWithEasyOCR(img_c)
showBoxes(img_c, results)
