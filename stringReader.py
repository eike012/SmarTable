# Returns the numbers of dollar signs and numbers in a string
def countDollarSignNumbers(input_string):
    numberAndDollarSign = 0
    for character in input_string:
        if (character.isnumeric()) or (character == '$'):
            numberAndDollarSign += 1
        
    return numberAndDollarSign

# Returns the result of a string with a dollar sign
def hasDollarSign(input_string):
    for i in range(len(input_string) - 1, -1, -1):
        if input_string[i] == "$":
            return True, input_string[:i-1], input_string[i-1:len(input_string)]
        
    return False, input_string, ""

# Removes special characters
def removeMarks(input_string):
    output_string = ""

    marks = [".", "-", "?", "!", "&", ":", ";", "/", "[", "]", "{", "}"] # characters to remove
    for character in range(len(input_string)):
        if input_string[character] in marks:
            continue
        else:
            output_string = output_string + input_string[character]

    return output_string 

# Returns whether a string has at least one number or letter
def hasLetterorNumber(input_string):
    for character in input_string:
        if character.isnumeric() or character.isalpha():
            return True
    
    return False

# Returns whether a string has many numerical values or not
def hasManyNumbers(input_string):
    count = 0
    for character in input_string:
        if character.isnumeric():
            count += 1

    if count/ len(input_string) > 0.5:    
        return True

    return False

# Returns the ratio of lower case letters on a string
def ratioLowerCase(input_string):
    totalLetters = len(input_string)
    lowerCase = 0

    for character in input_string:
        if character.islower():
            lowerCase += 1
    
    if totalLetters == 0:
        return 0
    return lowerCase/totalLetters

# Small test of functions
def testProgram():
    assert ratioLowerCase('Asaa') == 0.75, 'Erro em ratioLowerCase, teste 1'
    assert countDollarSignNumbers('R$22,00') == 5, 'Erro em countDollarSignNumbers, teste 2'
    assert ratioLowerCase('AAA') == 0.00, 'Erro em ratioLowerCase, teste 3'
    assert countDollarSignNumbers('pizza') == 0.00, 'Erro em countDollarSignNumbers, teste 4'
    assert removeMarks("Hoje tem trikas.") == "Hoje tem trikas", 'Erro em removeMarks, teste 5'
    assert removeMarks("Nao. Durma. Na. Aula!") == "Nao Durma Na Aula", 'Erro em removeMarks, teste 6'

testProgram()