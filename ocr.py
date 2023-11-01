import re 
import enchant
import easyocr
import pytesseract
import json
import cv2
from PIL import Image, ImageDraw
import quicksort as qs
import preprocess as pp
import math
import kmeans
import statistics
import stringReader as sr

img = 'images/image.png'
section_img = 'images/section.png'

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
    results,_,_ = processImageWithEasyOCR(img)
    # print(confidence)
    # print("Width:\n")
    # arraywidth = arrayWidthOfBoxes(results)
    # print(arraywidth)
    # print("Height:\n")
    # arrayheight = arrayHeightOfBoxes(results)
    # print(arrayheight)
    # print("Area:\n")
    # arrayarea = arrayAreaOfBoxes(results)
    # print(arrayarea)
    # print("Kmeans of width:\n")
    # print(kmeans.kmeansOfArray1D(arraywidth))
    # print("Kmeans of height:\n")
    # print(kmeans.kmeansOfArray1D(arrayheight))
    # print("Kmeans of area:\n")
    # print(kmeans.kmeansOfArray1D(arrayarea))
    # print("Lowercase ratio:\n")
    arrayMinusculo = arrayLowerCaseAndNumbers(results)
    # print(arrayMinusculo)
    # print("Labels minuscula + numeros:\n")
    labels = kmeans.kmeansOfArray2D(arrayMinusculo)
    # for i in range(len(labels)):
    #     print(f"Category of {results[i][1]}: {labels[i]}")
    number_of_columns = numberColumnsImage(results, labels)
    print(f"\n Number of columns: {number_of_columns}")
    image = Image.open(img)
    width, height = image.size
    part_width = width // number_of_columns

    for i in range(number_of_columns):
        left = i * part_width
        right = (i + 1) * part_width
        section = image.crop((left, 0, right, height))

        section.save(section_img)
        results, confidence, element_array = processImageWithEasyOCR(section_img)
        showBoxes(section_img, results)
        arrayMinusculo = arrayLowerCaseAndNumbers(results)
        labels = kmeans.kmeansOfArray2D(arrayMinusculo)
        createJson(element_array, labels)
    return confidence

# Calculate the number of columns within a menu
def numberColumnsImage(results, labels):

    for i in range(len(labels)):
        if labels[i] == "Recipe":
            beginningSecondLoop = i
            break

    lastTitle  = -1
    titlesPerLine = []
    numberTitles = 0

    for j in range(beginningSecondLoop, len(labels)):
        if labels[j] == "Title" and results[j][1].isnumeric():
            continue
        else:
            if labels[j] == "Title" and lastTitle == -1:
                lastTitle = j
                numberTitles += 1
                continue
            if labels[j] == "Title" and not results[j][1].isnumeric():
                if boxIsNewLine(results[j], results[lastTitle]):
                    titlesPerLine.append(numberTitles)
                    numberTitles = 1
                else:
                    numberTitles += 1
                lastTitle = j
                    
    print(f"\nTotal of titles per line: {titlesPerLine}")

    mode = statistics.mode(titlesPerLine)
    return mode   


# Get the average value of an array
def averageOfArray(array1D):
    totalSum = 0
    quantity = len(array1D)

    for element in array1D:
        totalSum += element

    return totalSum/quantity

# Check if subsequential boxes make up a new line
def boxIsNewLine(box1, box2):
    p0, p1, p2, p3 = box1[0]
    d0, d1, d2, d3 = box2[0]

    if d0[1] in range(round(p0[1]),round(p2[1])) or p0[1] in range(round(d0[1]),round(d2[1])):
        return False

    return True

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

# Check whether box is going to get used or not
def checkBox(height, width):
    if height <= width:
        return True
    
    return False

def processImageWithEasyOCR(img):
    # Initialize EasyOCR reader
    reader = easyocr.Reader(['pt'])
    dic = enchant.Dict('pt_BR')
    addDic(dic)

    # Process the entire image using EasyOCR
    results = reader.readtext(img)
    probMean = 0

    coordinates ,filtered_results = [], []
    # Print EasyOCR results for the entire image
    for (bbox,_, prob) in results:
        x_coordinates = [int(bbox[0][0]),int(bbox[1][0])]
        y_coordinates = [int(bbox[0][1]),int(bbox[2][1])]
        width = x_coordinates[1] - x_coordinates[0]
        height = y_coordinates[1] - y_coordinates[0]
    
        if checkBox(height, width):
            filtered_results.append((bbox, _, prob))
            probMean += prob
            coordinates.append([x_coordinates,y_coordinates])

    element_array = processImageWithTesseractOCR(img, coordinates, dic)
    
    return filtered_results, probMean/len(filtered_results), element_array

# Process individual images using TesseractOCR
def processImageWithTesseractOCR(image_path, coordinates, dic):
    img = cv2.imread(image_path)
    custom_config = "-l por --oem 3 --psm 6"

    qs.quickSort(coordinates, 0, len(coordinates)-1)
    element_array = []

    for x, y in coordinates:
        cropped_image = img[y[0]:y[1],x[0]:x[1]]

        text = pytesseract.image_to_string(cropped_image, config=custom_config)
        new_text = checkGrammar(text, dic)
        new_text = re.sub(r'\s+', ' ', new_text.strip())

        element_array.append(new_text)

    return element_array

# Reset title, recipe and prices variables
def resetCategories():
    return "","",[]

# Return output data to insert into the json file
def returnData(title, recipe, prices):
    output_data = []
    output_dict = {"Title": title, "Recipe": recipe}
    index = 1
    for price in prices:
        output_dict[f"Price {index}"] = price
        index += 1
    output_data.append(output_dict.copy())
    return output_data

# Create json file to have each item in the menu
def createJson(array, labels):
    json_path = "categories.json"
    output = []
    title, recipe, prices = resetCategories()
    for i in range(len(array)):
        print(f"{array[i]} = {labels[i]}")
        if labels[i] == "Title":
            if title != "":
                if sr.ratioLowerCase(array[i]) == 0:
                    title = array[i]
                else:
                    recipe = array[i] + " "
                continue
            else: 
                title = array[i]
        elif labels[i] == "Recipe":
            recipe += array[i]
        else:
            prices.append(array[i])
        if title != "" and recipe != "" and len(prices) != 0:
            output_data = returnData(title, recipe, prices)
            output.append(output_data)
            title, recipe, prices = resetCategories()

    with open(json_path, 'w') as json_file:
        json.dump(output, json_file, indent=4)

# Return the width of easyOCR boxes as an array
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

# Return the height of easyOCR boxes as an array
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

# Return the area of easyOCR boxes as an array
def arrayAreaOfBoxes(bounds):
    arrayHeight = arrayHeightOfBoxes(bounds)
    arrayWidth = arrayWidthOfBoxes(bounds)
    arrayArea = []

    for i in range(len(arrayHeight)):
        area = arrayHeight[i]*arrayWidth[i]
        arrayArea.append(area)

    return arrayArea

# Return an array with a tuple = {ratio of lower case letters, quantity of numbers}
# for each box read by ocr
def arrayLowerCaseAndNumbers(ocrResults):
    arrayResult = []

    for box in ocrResults:
        readString = box[1]
        tupleResult = [sr.ratioLowerCase(readString) * 3, sr.countDollarSignNumbers(readString)]
        arrayResult.append(tupleResult)

    return arrayResult



