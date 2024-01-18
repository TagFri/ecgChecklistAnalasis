import csv
def readCSV(filename):
    f = open(filename, "r")
    data = list(csv.reader(f, delimiter=","))
    fullDatabase = [row for row in data]
    f.close()
    return(fullDatabase)

def writeCSV(filename, list_of_lists):
    f = open(filename, 'w')
    writer = csv.writer(f)
    for row in list_of_lists:
        writer.writerow(row)
    return(print(f'CSV export to {filename} is complete'))

def saveHeaderAsList(listOfLists):
    headerVaraibles = []
    for row in listOfLists[0]:
        headerVaraibles.append(row)
    return(headerVaraibles)

def mappingIndex2Column(startIndex, headerlist):
    mapping = {}
    index = startIndex
    for column in headerlist:
        mapping[index] = column
        index += 1
    return(mapping)

def mappingColumn2Index(startIndex, headerlist):
    mapping = {}
    index = startIndex
    for column in headerlist:
        mapping[column] = index
        index += 1
    return (mapping)