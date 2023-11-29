def dishCheck(JSONArray, referenceArray):
    count = 0
    for i in range(len(JSONArray)):
        if len(JSONArray[i][0]) == 3:
            cmpTitle = JSONArray[i][0]['Title']
            cmpPrice = JSONArray[i][0]['Price 1']
            for j in range(len(referenceArray)):
                if cmpTitle == referenceArray[j][0]['Title'] and cmpPrice == referenceArray[j][0]['Price 1']:
                    count += 1
        else:
            cmpTitle = JSONArray[i][0]['Title']
            cmpPrice1 = JSONArray[i][0]['Price 1']
            cmpPrice2 = JSONArray[i][0]['Price 2']
            for j in range(len(referenceArray)):
                if cmpTitle == referenceArray[j][0]['Title'] and cmpPrice1 == referenceArray[j][0]['Price 1'] and cmpPrice2 == referenceArray[j][0]['Price 2']:
                    count += 1
    
    return 100*count/len(JSONArray)

