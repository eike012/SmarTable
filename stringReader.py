#returns the numbers of dollar signs and numbers in a string
def countDollarSignNumbers(input_string):
    numberAndDollarSign = 0
    for character in input_string:
        if (character.isnumeric()) or (character == '$'):
            numberAndDollarSign += 1
        
    return numberAndDollarSign

#returns length of string
def stringLength(input_string):
    return len(input_string)

#returns the ratio of lower case letters on a string
def ratioLowerCase(input_string):
    totalLetters = len(input_string)
    lowerCase = 0

    for character in input_string:
        if character.islower():
            lowerCase += 1
    
    if totalLetters == 0:
        return 0
    return lowerCase/totalLetters

def testProgram():
    assert ratioLowerCase('Asaa') == 0.75, 'Erro em ratioLowerCase, teste 1'
    assert countDollarSignNumbers('R$22,00') == 5, 'Erro em countDollarSignNumbers, teste 2'
    assert ratioLowerCase('AAA') == 0.00, 'Erro em ratioLowerCase, teste 3'
    assert countDollarSignNumbers('pizza') == 0.00, 'Erro em countDollarSignNumbers, teste 4'

testProgram()