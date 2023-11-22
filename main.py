import ocr

img_a = 'images/a.jpg'
img_alemao = 'images/alemao.jpeg'
img_b = 'images/b.jpg'
img_c = 'images/c.jpg'
img_d = 'images/d.jpeg'
img_e = 'images/e.jpeg'
img_f = 'images/f.jpeg'
img_g = 'images/g.jpeg'
img_l = 'images/l.jpg'
img_l2 = 'images/l2.jpg'
plano = 'images/plano.jpeg'


def main():
    choice = 0
    results, confidence, element_array = ocr.checkConfidence(img_l) 
    print(confidence)

    # Check whether confidence is above desirable percentage
    while confidence < 0.8 and choice == 0:
        if confidence < 0.8:   
            # Take another picture
            choice = int(input("Confidence below 80%. Continue?: "))
            if choice == 0:
                #img = newFoto()
                results, confidence = ocr.checkConfidence(img_b) 
        else:
            choice = 1
    
    ocr.readText(results, element_array)
    
        
if __name__ == "__main__":
         main()