import re 
import enchant
import easyocr
import pytesseract
import logisticRegression as lr
import joblib
import json
import cv2
from PIL import Image, ImageDraw
import quicksort as qs
import preprocess as pp
import math
import kmeans

img = 'images/image.png'

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
    results, confidence = processImageWithEasyOCR(img)
    showBoxes(img, results)
    print(confidence)
    print("Width:\n")
    arraywidth = arrayWidthOfBoxes(results)
    print(arraywidth)
    print("Height:\n")
    arrayheight = arrayHeightOfBoxes(results)
    print(arrayheight)
    print("Area:\n")
    arrayarea = arrayAreaOfBoxes(results)
    print(arrayarea)
    print("Kmeans of width:\n")
    print(kmeans.kmeansOfArray1D(arraywidth))
    print("Kmeans of height:\n")
    print(kmeans.kmeansOfArray1D(arrayheight))
    print("Kmeans of area:\n")
    print(kmeans.kmeansOfArray1D(arrayarea))

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
                # print(f"'{word}' is spelled correctly.")
                pass
            else:
                suggestions = dic.suggest(word)
                if suggestions != None:
                    #print(f"'{word}' is spelled incorrectly. Suggestions: {', '.join(suggestions)}")
                    # words[index] = suggestions[0]
                    pass
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
    
    return results, probMean/len(results)

# Process individual images using TesseractOCR
def processImageWithTesseractOCR(image_path, coordinates, dic):
    img = cv2.imread(image_path)
    custom_config = "-l por --oem 3 --psm 6"

    final_text = ''
    qs.quickSort(coordinates, 0, len(coordinates)-1)
    element_array = []

    for x, y in coordinates:
        cropped_image = img[y[0]:y[1],x[0]:x[1]]

        text = pytesseract.image_to_string(cropped_image, config=custom_config)
        new_text = checkGrammar(text, dic)
        new_text = re.sub(r'\s+', ' ', new_text.strip())

        element_array.append(new_text)
        final_text += new_text + " "

    createJson(element_array)
    return final_text

def resetCategories():
    return "","",[]

def returnData(title, recipe, prices):
    output_data = []
    output_dict = {"Title": title, "Recipe": recipe}
    index = 1
    for price in prices:
        output_dict[f"Price {index}"] = price
        index += 1
    output_data.append(output_dict.copy())
    return output_data

def createJson(array):
    json_path = "categories.json"
    output = []
    lr.train()
    title, recipe, prices = resetCategories()
    classifier = joblib.load('classifier.pkl')
    for text in array:
        text_vectorized = lr.tfidf_vectorizer.transform([text])
        category = classifier.predict(text_vectorized)
        print(f"Predicted Category for {text}: {category[0]}")
        if category == "Title":
            if title != "":
                recipe = text + " "
                continue
            else: 
                title = text
        elif category == "Recipe":
            recipe += text
        else:
            prices.append(text)
        if title != "" and recipe != "" and len(prices) != 0:
            output_data = returnData(title, recipe, prices)
            output.append(output_data)
            title, recipe, prices = resetCategories()
    
    with open(json_path, 'w') as json_file:
        json.dump(output, json_file, indent=4)

#Return the width of easyOCR boxes as an array
def arrayWidthOfBoxes(bounds):
    boundsLength = len(bounds)
    arrayWidth = []
    
    for i in range(boundsLength):
        p0, p1, p2, p3 = bounds[i][0]
        width_superior = math.sqrt(((p1[0] -  p0[0])**2) + ((p1[1] - p0[1])**2))
        width_inferior = math.sqrt(((p2[0] -  p3[0])**2) + ((p2[1] - p3[1])**2))
        width = (width_superior + width_inferior)/2
        arrayWidth.append(width)
      
    return arrayWidth    

#Return the height of easyOCR boxes as an array
def arrayHeightOfBoxes(bounds):
    boundsLength = len(bounds)
    arrayHeight = []
    
    for i in range(boundsLength):
        p0, p1, p2, p3 = bounds[i][0]
        height_right = math.sqrt(((p2[0] -  p1[0])**2) + ((p2[1] - p1[1])**2))
        height_left = math.sqrt(((p0[0] -  p3[0])**2) + ((p0[1] - p3[1])**2))
        height = (height_right + height_left)/2
        arrayHeight.append(height)
      
    return arrayHeight  

#Return the area of easyOCR boxes as an array
def arrayAreaOfBoxes(bounds):
    arrayHeight = arrayHeightOfBoxes(bounds)
    arrayWidth = arrayWidthOfBoxes(bounds)
    arrayArea = []

    for i in range(len(arrayHeight)):
        area = arrayHeight[i]*arrayWidth[i]
        arrayArea.append(area)

    return arrayArea
    
checkImageQuality(img)