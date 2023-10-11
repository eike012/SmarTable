import numpy as np
from sklearn.cluster import KMeans

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

    print("price, recipe, title:" + str(price) + " " + str(recipe) + " " + str(title) + "\n")
    return names
