import ocr
import json
import numpy as np
import dishcheck as dc

def check(letter):
    image = f'images/{letter}.jpg'
    json_file_path = f'testJsons/{letter}.json'
    results, _, element_array = ocr.checkConfidence(image) 
    array_to_check = ocr.readText(results, element_array, True)
    with open(json_file_path, 'r') as file:
        reference_array = json.load(file)
    percentage = dc.dishCheck(array_to_check, reference_array)

    return percentage

def test():
    images_to_test = ['a','b','c']
    results = []
    print("Testing.....")
    for letter in images_to_test:
        result = check(letter)
        print(f"Percentage of tests passed for image {letter}.jpg is: {result}%")
        results.append(result)
    
    print(f"\n\nThe average percentage of tests passed is: {np.mean(results)}%")
        
test()