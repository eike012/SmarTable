import cv2 
import pytesseract
import numpy as np
from pytesseract import Output
import easyocr
import matplotlib.pyplot as plt 
from PIL import Image, ImageDraw

# Get grayscale image
def getGrayScale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Noise removal
def removeNoise(image):
    return cv2.fastNlMeansDenoising(image, None, 10, 7, 21)

# Thresholding
def thresholding(grayScaleImage):
    image = cv2.adaptiveThreshold(grayScaleImage,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,2)
    return image

# Opening - erosion followed by dilation
def dilate(image):
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(image, kernel, iterations=200)
    return img

def erode(image):
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.erode(image, kernel, iterations=1)
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
    #img = cv2.GaussianBlur(img, (3, 3), 0)
    #gray = getGrayScale(img)
    #cv2.imwrite('tests/gray.png',gray)
    # deskewed = deskew(gray)
    # cv2.imwrite('tests/deskewed.png',deskewed)
    #denoised = removeNoise(gray)
    #cv2.imwrite('tests/denoised.png',denoised)
    eroded = erode(img)
    dilated = dilate(eroded)
    cv2.imwrite('tests/dilated_eroded.png', dilated)
    # cv2.imwrite('tests/opening.png',open)
    # thresh = thresholding(open)
    # cv2.imwrite('tests/thresh.png',thresh)
    # can = canny(thresh)
    # cv2.imwrite('tests/canny.png',can)
    return open

# Show boxes of text of image
def showBoxes(img):
    h, w = img.shape
    boxes = pytesseract.image_to_boxes(img) 
    for b in boxes.splitlines():
        b = b.split(' ')
        img = cv2.rectangle(img, (int(b[1]), h - int(b[2])), (int(b[3]), h - int(b[4])), (0, 255, 0), 2)

    cv2.imshow('img', img)
    cv2.waitKey(0)

#applyTesseract(img_alemao)

# func to apply transformation and visualize the result

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

#plt.imshow(img_alemao[:,:,::-1])
#plt.axis('off')


#detectBorder

#function that gets an image and saves another one with the most external border drawn

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
    



def rotate(img_lida):
    endereco_teste = 'teste.png'
    img = Image.open(img_lida)
    angle = 4
    img2 = img.rotate(angle)
    img2.save(endereco_teste)
    img2.show()
    results = avgPrecisionProcessImageWithEasyOCR(endereco_teste)
    showBoxes(endereco_teste,results)

def perform_Transformation(image, M):
    """
    Takes in input image and the transformation matrix 
    Appl
    """
    rows,cols,ch = image.shape

    dst = cv2.warpAffine(image,M,(cols,rows))
    cv2.imwrite('alemao_rotado.jpg', dst)
    

# M = np.float32([[1,0.02,0],
                # [-0.01,1,0]])
# 
# perform_Transformation(img_alemao, M)

def avgPrecisionProcessImageWithEasyOCR(img):
    # Initialize EasyOCR reader
    reader = easyocr.Reader(['pt'])

    # Process the entire image using EasyOCR
    results = reader.readtext(img)

    # Print EasyOCR results for the entire image
    prob_total = 0
    total_de_probs = 0
    for (bbox, text, prob) in results:
        print(f"Text: {text}, Confidence: {prob}\n")
        prob_total += prob
        total_de_probs += 1
    
    media = prob_total/total_de_probs
    print("media: ", media)

    return prob_total/total_de_probs

def projectTransformation(img):
    image = cv2.imread(img)
    num_cols = image.shape[0]
    num_rows = image.shape[1]
    src_points = np.float32([[0,0], [num_cols-1,0], [0,num_rows-1], [num_cols-1,num_rows-1]])
    dst_points = np.float32([[0,0], [int(0.999*(num_cols-1)),0], [0,num_rows-1], [num_cols-1,num_rows-1]])
    projective_matrix = cv2.getPerspectiveTransform(src_points, dst_points)
    img_protran = cv2.warpPerspective(image, projective_matrix, (num_cols,num_rows))
    cv2.imwrite('alemao_trap.jpg', img_protran)

#image = preProcess(img_alemao)
#processImageWithEasyOCR('tests/dilated.png')
#imagegrayScale = getGrayScale('images/alemao.jpeg')
#cv2.imwrite('grayScaleimage.jpg', imagegrayScale)
#image = removeNoise('grayScaleimage.jpg')
#cv2.imwrite('denoised_alemao.jpg', image)
#projectTransformation('images/alemao.jpeg')
#testaPrecisaoEasyOCR('images/alemao.jpeg')
#processImageWithEasyOCR('alemao_trap.jpg')
#rotate('images/alemao.jpeg')
# image = preProcess(img_a)
# applyTesseract(image)
# #showBoxes(image)
# image = preProcess(img_alemao)
# applyTesseract(image)
# #showBoxes(image)
# image = preProcess(img_b)
# applyTesseract(image)
# #showBoxes(image)
#image = preProcess(img_c)
#applyTesseract(image)
#showBoxes(image)
#detectBorder(img_alemao)