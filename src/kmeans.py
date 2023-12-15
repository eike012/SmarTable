import numpy as np
from sklearn.cluster import KMeans

# Gets a list of numbers and splits them into 3 classes
def kmeansOfArray1D(dataOfBoxes):
    result = np.array(dataOfBoxes).reshape(-1,1)
    kmeans = KMeans(n_clusters=3, random_state=0, n_init="auto").fit(result)
    labels = kmeans.labels_
    names = []
    price = 0
    title = 0
    recipe = 0
    for item in labels:
        if item == 0:
            names.append('Price')
            price += 1
        elif item == 1:
            names.append('Title')
            title += 1
        else:
            names.append('Recipe')
            recipe += 1

    return names

# Gets an array of points (x, y) and splits them into 3 classes:
# Title, Recipe and Price.
def kmeansOfArray2D(dataofBoxes):
    result = dataofBoxes
    kmeans = KMeans(n_clusters=3, random_state=0, n_init="auto").fit(result)
    labels = kmeans.labels_

    maxRatio = 0
    maxNumbers = 0
    indexMaxRatio = -1
    indexMaxNumbers = -1
    for i in range(len(dataofBoxes)):
        if dataofBoxes[i][0] > maxRatio:
            maxRatio = dataofBoxes[i][0]
            indexMaxRatio = i
        if dataofBoxes[i][1] > maxNumbers:
            maxNumbers = dataofBoxes[i][1]
            indexMaxNumbers = i

    valueRecipe = labels[indexMaxRatio]
    valuePrice = labels[indexMaxNumbers]

    names = []
    for k in labels:
        if k == valueRecipe:
            names.append('Recipe')
        elif k == valuePrice:
            names.append('Price')
        else:
            names.append('Title')

            
    return names