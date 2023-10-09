import re 
import enchant
import easyocr
import pytesseract
import cv2
from PIL import Image, ImageDraw
import quicksort as qs
import preprocess as pp

img = 'images/c.jpg'

# Show boxes of text of image
def showBoxes(img, bounds, color="yellow", width=2):
    image = Image.open(img)
    draw = ImageDraw.Draw(image)
    for bound in bounds:
        p0, p1, p2 , p3 = bound[0]
        draw.line([*p0, *p1, *p2, *p3, *p0], fill=color, width=width)
    
    image.show()

# Get results from the image
def checkImageQuality(image):
    pp.preProcess(image)
    results, confidence, text = processImageWithEasyOCR(img)
    showBoxes(img, results)
    print(text)
    print(confidence)
    return results, confidence

# Add missing words to the dictionary
def addDic(dic):
    dict_path = 'dictWords.txt'
    try:
        with open(dict_path, 'r') as file:
            for word in file:
                dic.add(word)

    except FileNotFoundError:
        print(f"File '{dict_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Check the spelling of every word
def checkGrammar(text, dic):    
    regex = '[^a-zA-Z0-9$]+'
    words = re.split(regex,text)
    # Check the spelling of a word
    for index, word in enumerate(words):
        if word != '' and not word.isnumeric():
            if  dic.check(word):
                print(f"'{word}' is spelled correctly.")
            else:
                suggestions = dic.suggest(word)
                if suggestions != None:
                    print(f"'{word}' is spelled incorrectly. Suggestions: {', '.join(suggestions)}")
                # words[index] = suggestions[0]
            if word == "RS":
                word = word.replace('RS','R$')

    output = ''.join([value + sep for value, sep in zip(words, re.findall(regex, text))]) + words[-1]
    return output

def processImageWithEasyOCR(img):
    # Initialize EasyOCR reader
    reader = easyocr.Reader(['pt'])
    dic = enchant.Dict('pt_BR')
    addDic(dic)

    # Process the entire image using EasyOCR
    results = reader.readtext(img)
    probMean = 0

    coordinates = []
    # Print EasyOCR results for the entire image
    for (bbox,_, prob) in results:
        probMean += prob
        x_coordinates = [int(bbox[0][0]),int(bbox[1][0])]
        y_coordinates = [int(bbox[0][1]),int(bbox[2][1])]
        coordinates.append([x_coordinates,y_coordinates])

    text = processImageWithTesseractOCR(img, coordinates, dic)
    output_file = 'output.txt'
    with open(output_file, 'w', encoding='utf8') as file:
        file.write(text)
    
    return results, probMean/len(results), text

# Process individual images using TesseractOCR
def processImageWithTesseractOCR(image_path, coordinates, dic):
    img = cv2.imread(image_path)
    custom_config = "-l por --oem 3 --psm 6"

    final_text = ''
    qs.quickSort(coordinates, 0, len(coordinates)-1)

    for x, y in coordinates:
        cropped_image = img[y[0]:y[1],x[0]:x[1]]

        text = pytesseract.image_to_string(cropped_image, config=custom_config)
        new_test = checkGrammar(text, dic)
        final_text += new_test

    return final_text

#Return the width of easyOCR boxes as an array
def arrayWidthOfBoxes(bounds):
    boundsLength = len(bounds)
    arrayWidth = []
    
    for i in range(boundsLength):
        p0, p1, p2, p3 = bounds[i][0]
        width_superior = sqrt(((p1[0] -  p0[0])**2) + ((p1[1] - p0[1])**2))
        width_inferior = sqrt(((p2[0] -  p3[0])**2) + ((p2[1] - p3[1])**2))
        width = (width_superior + width_inferior)/2
        arrayWidth.append(width)
      
    return arrayWidth    

#Return the height of easyOCR boxes as an array
def arrayHeightOfBoxes(bounds):
    boundsLength = len(bounds)
    arrayHeight = []
    
    for i in range(boundsLength):
        p0, p1, p2, p3 = bounds[i][0]
        height_right = sqrt(((p2[0] -  p1[0])**2) + ((p2[1] - p1[1])**2))
        height_left = sqrt(((p0[0] -  p3[0])**2) + ((p0[1] - p3[1])**2))
        height = (height_right + height_left)/2
        arrayHeight.append(height)
      
    return arrayHeight  

#Return the area of easyOCR boxes as an array
def arrayAreaOfBoxes(bounds):
    arrayHeight = arrayAreaOfBoxes(bounds)
    arrayWidth = arrayWidthOfBoxes(bounds)
    arrayArea = []

    for i in range(len(arrayHeight)):
        area = arrayHeight[i]*arrayWidth[i]
        arrayArea.append(area)

    return arrayArea
    
checkImageQuality(img)