import re 
import enchant
import easyocr
import pytesseract
import json
import cv2
from PIL import Image, ImageDraw
import quicksort as qs
import preprocess as pp
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

# Get confidence from the text of the image
def checkConfidence(image):
    pp.preProcess(image)
    results,_,element_array = processImageWithEasyOCR(img)
    confidence_scores = [result[2] for result in results]
    average_confidence = sum(confidence_scores) / len(confidence_scores)
    return results, average_confidence, element_array

# Get number of columns of image and prices per dish
def getColumnsandPrices(results):
    number_of_columns, number_of_prices = numberColumnsImage(results, kmeans.kmeansOfArray2D((arrayLowerCaseAndNumbers(results))))

    print(f"\nThe number of columns found is: {number_of_columns}")
    choice = int(input("\nPress 0 to accept or 1 to type another number: "))
    if choice:
        number_of_columns = int(input("\nType how many columns the menu has: "))
    print(f"\nNumber of prices: {number_of_prices}")
    choice = int(input("\nPress 0 to accept or 1 to type another number: "))
    if choice:
        number_of_prices = int(input("\nType how many prices per dish the menu has: "))

    return number_of_columns, number_of_prices

# Read the text with EasyOCR and TesseractOCR
def readText(results, element_array):
    number_of_columns, number_of_prices = getColumnsandPrices(results)
    image = Image.open(img)
    width, height = image.size
    part_width = width // number_of_columns

    elements, kmean = [], []

    for i in range(number_of_columns):
        left = i * part_width
        right = (i + 1) * part_width
        section = image.crop((left, 0, right, height))

        section.save(section_img)
        results, _, element_array = processImageWithEasyOCR(section_img)
        elements = elements + element_array
        showBoxes(section_img, results)
        arrayMinusculo = arrayLowerCaseAndNumbers(element_array)
        kmean = kmean + kmeans.kmeansOfArray2D(arrayMinusculo)

    createJson(elements, kmean, number_of_prices)

# Calculate the number of columns within a menu
def numberColumnsImage(results, labels):

    for i in range(len(labels)):
        if labels[i] == "Recipe":
            beginningSecondLoop = i
            break

    lastTitle  = -1
    titlesPerLine, pricesPerLine = [], []
    numberTitles, numberPrices = 0, 0

    for j in range(beginningSecondLoop, len(labels)):
        if labels[j] == "Title" and results[j][1].isnumeric():
            continue
        else:
            if labels[j] == "Title" and lastTitle == -1:
                lastTitle = j
                numberTitles += 1
                continue
            if labels[j] == "Title" and not results[j][1].isnumeric():
                if numberPrices > 0:
                    pricesPerLine.append(numberPrices)
                    numberPrices = 0
                if boxIsNewLine(results[j], results[lastTitle]):
                    titlesPerLine.append(numberTitles)
                    numberTitles = 1
                else:
                    numberTitles += 1
                lastTitle = j
            elif labels[j] == "Price":
                numberPrices += 1
    
    # print(f"\nTotal of prices per line: {pricesPerLine}")
    # print(f"\nTotal of titles per line: {titlesPerLine}")

    titles_mode = statistics.mode(titlesPerLine)
    prices_mode = statistics.mode(pricesPerLine)

    return titles_mode, prices_mode   


# Get the average value of an array
def averageOfArray(array1D):
    totalSum = 0
    quantity = len(array1D)

    for element in array1D:
        totalSum += element

    return totalSum/quantity

# Check if subsequential boxes make up a new line
def boxIsNewLine(box1, box2):
    p0, _, p2, _ = box1[0]
    d0, _, d2, _ = box2[0]

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
                words[index] = "R$"

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
    return "","",[],0

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

# Create object with all categories 
def createObject(output, title, recipe, prices, number_of_prices, overread_prices):
    output_data = returnData(title, recipe, prices)
    output.append(output_data)
    title, recipe, prices, prices_read = resetCategories()
    if len(overread_prices) > 0:
        index = 0
        while len(overread_prices) != 0 and index < number_of_prices:
            prices.append(overread_prices[0])
            overread_prices.pop(0)
            index += 1 
    return output, title, recipe, prices, prices_read, overread_prices

# Create json file to have each item in the menu
def createJson(array, labels, number_of_prices):
    json_path = "categories.json"
    output = []
    title, recipe, prices, prices_read = resetCategories()
    overread_prices = []

    for i in range(len(array)):
        print(f"{array[i]} = {labels[i]}")
        if sr.hasLetterorNumber(array[i]):
            prices_read = len(prices)
            if len(array[i]) > 10:
                has_sign, array[i], price_merged = sr.hasDollarSign(array[i])
                if has_sign:
                    output, title, recipe, prices, prices_read, overread_prices = createObject(output, title, recipe, prices, number_of_prices, overread_prices)
                    labels[i] = "Title"
                if len(price_merged) > 3:
                    if prices_read < number_of_prices:
                        prices.append(price_merged)
                    else:
                        overread_prices.append(price_merged)
            if labels[i] == "Title" and len(array[i]) > 3 and not sr.hasManyNumbers(array[i]) and array[i] != "R$":
                if title != "":
                    if sr.ratioLowerCase(array[i]) == 0:
                        title = array[i]
                    else:
                        recipe = array[i] + " "
                    continue
                else: 
                    title = array[i]
            elif labels[i] == "Recipe" and title != "" and len(array[i]) > 3:
                recipe += array[i] + " "
            elif labels[i] == "Price" and 3 < len(array[i]) < 10:
                if prices_read < number_of_prices:
                    prices.append(array[i])
                else:
                    overread_prices.append(array[i])
            if i == len(array)-1 or (title != "" and recipe != "" and len(prices) != 0 and labels[i+1] == "Title"):
                output, title, recipe, prices, prices_read, overread_prices = createObject(output, title, recipe, prices, number_of_prices, overread_prices)
                                

    with open(json_path, 'w') as json_file:
        json.dump(output, json_file, indent=4, ensure_ascii=False)

# Return an array with a tuple = {ratio of lower case letters, quantity of numbers}
# for each box read by ocr
def arrayLowerCaseAndNumbers(array):
    arrayResult = []
    for words in array:
        if type(words) == tuple:
            word = words[1]
        else:
            word = words
        tupleResult = [sr.ratioLowerCase(word) * 3, sr.countDollarSignNumbers(word)]
        arrayResult.append(tupleResult)

    return arrayResult



