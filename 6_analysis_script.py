#--------------------------
### IMPORT DEPENDENCIES
#--------------------------
from pythonModules.csvModule import readCSV
from pythonModules.csvModule import writeCSV
from pythonModules.csvModule import saveHeaderAsList
from pythonModules.csvModule import mappingIndex2Column
from pythonModules.csvModule import mappingColumn2Index
from itertools import combinations

#--------------------------
### DICTIONARIES
#--------------------------
#Values to normalize each variable value to either 'normal' == columnInteger[0] or 'abnormal' == columnInteger[1]
normalization = {
    3: [["y"], ["n"]], #p_before_qrs
    4: [["r"], ["u"]], #rhythem
    5: [["normal"], ["takycardia","bradycardia"]],  # frequency
    6: [["normal"], ["prolonged","shosrt"]],  # qrs_time
    7: [["normal"], ["prolonged","short","abnormal"]],  # p_interval
    8: [["no"], ["yes"]],  # st_elevation
    9: [["no"], ["yes"]],  # st_depression
    10: [["no"], ["yes"]],  # t-inversion
    11: [["n"], ["l","r","ex"]],  # axis
    12: [["no"], ["yes"]],  # sokolow
    13: [["no"], ["yes"]],  # cornell
    14: [["normal","N/A"], ["abnormal"]],  # p_intervall
    15: [["no"], ["yes"]],  # t_peak
    16: [["no"], ["yes"]],  # t_biphasic
    17: [["no"], ["yes"]],  # u-inversion
    18: [["no"], ["yes"]],  # u-amplitude
}

#--------------------------
### FUNCTIONS
#--------------------------
### INTER-INTERPRETATION VARIANCE

def variance_calculation(checklist1, checklist2):
    assert len(checklist1) == len(checklist2)

    #List all variables in table from column 3 and out:
    variables = saveHeaderAsList(checklist1)[3:]

    ##Dictionary to track variance
    variances = {}
    for i in range(3,22):
        variances[i] = 0

    ##CALCULATING VARIANCE
    #Loop through all ECG's
    for ecg in range(1,309):
        #Loop through each variable for each ECG
        for variable in range(3,22):
            #of there is an discrepency, increase variance for that variable by 1
            if checklist1[ecg][variable] == checklist2[ecg][variable]:
                pass
            else:
                variances[variable] += 1

    #Map indexes and variable names
    mapping = mappingIndex2Column(3,variables)

    varianceList = []
    for column, variance in variances.items():
        varianceList.append([mapping[column],round(variance/(len(checklist1)-1),2)])

    return(varianceList)


### CLEANUP OF FINAL CHECKLIST
def checklist_cleanup(finalizedChecklist):
    cleansedChecklist = []
    #Attach first row of CSV file (variables)
    cleansedChecklist.append([finalizedChecklist[0][0], finalizedChecklist[0][1], finalizedChecklist[0][2], finalizedChecklist[0][4], finalizedChecklist[0][5], finalizedChecklist[0][7], finalizedChecklist[0][9], finalizedChecklist[0][11], finalizedChecklist[0][13], finalizedChecklist[0][15], finalizedChecklist[0][17], finalizedChecklist[0][18], finalizedChecklist[0][24],finalizedChecklist[0][26],finalizedChecklist[0][34], finalizedChecklist[0][38], finalizedChecklist[0][40], finalizedChecklist[0][42], finalizedChecklist[0][44]])
    #Add every secound row, and only applicable columns.
    #qtc, p-duration and p-amplitude are removed
    for row in finalizedChecklist[1::2]:
        cleansedChecklist.append([row[0], row[1], row[2], row[4], row[5], row[7], row[9], row[11], row[13], row[15], row[17], row[18], row[24], row[26],row[34], row[38], row[40], row[42], row[44]])
    return(cleansedChecklist)

### NORMALIZATION OF CLEANSED CHECKLIST
def checklist_normalisation(cleansedChecklist):
    normalchecklist = cleansedChecklist
    #Loop through all rows in finalizedChecklist except header
    for row in cleansedChecklist[1:]:
        #Start at column 3, as ID, gender and age are colum 0-2.
        for i in range(3,19):
            #if variable from csv is found in dictionary "normal values" assess csv variable to "1":
            if row[i] in normalization.get(i)[0]:
                row[i] = 1
            #if variable from csv is found in dictionary "abnormal values" assess csv variable to "0":
            elif row[i] in normalization.get(i)[1]:
                row[i] = 0
            #if variable from csv cannot be found in predefined values, assess csv variable to "ERROR"
            else:
                row[i] = "ERROR"
                assert row[i] != "ERROR"
    return(normalchecklist)

#--------------------------
### ANALASIS OF FINALIZED CHECKLIST
#--------------------------
#Get header variables from CSV, skipping first three and last column
def extract_all_header_variables(dataset):
    checklistpoints = []
    for checklistpoint in dataset[0][3:-1]:
        checklistpoints.append(checklistpoint)
    return(checklistpoints)

#Get all combinations of variables possible
def possible_combinations(variables):
    allPossibilities = []
    index = 1
    for i in range(1, numberOfPossibleVariables):
        combinationOfCertainNumberOfChecklistoints = list(combinations(variables, i))
        for oneSpecificCombination in combinationOfCertainNumberOfChecklistoints:
            cleanCombination = []
            for oneVariable in oneSpecificCombination:
                cleanCombination.append(oneVariable)
            allPossibilities.append([len(cleanCombination),cleanCombination,0,0])
    return(allPossibilities)

#Analyse all possibilities for all ECG's
def analyseChecklists(booleanChecklist, possibleChecklists, alfa):
    #Extract headervariables:
    variables = extract_all_header_variables(booleanChecklist)
    mapping = mappingColumn2Index(3,variables)

    #CALCULATE NUMBER OF ABNORMAL ECGS IN DATASET
    numberOfAbnormal = 0
    for row in booleanChecklist[1:]:
        counter = 0
        for variable in row[3:-1]:
            if int(variable) == 1:
                counter += 1
        if counter != len(variables):
            numberOfAbnormal +=1
    # PER POSSIBLE CHEKLIST: LOOP TRHUGH ALL ECG AND CHECK IF CHECKLIST CATCHES ABNOMRAL ECG OR NOT
    #Loop trhough all possible checklist combinations
    for possiblity in possibleChecklists:
        #Loop through all ECG's, skipping header row
        for row in booleanChecklist[1:]:
            #Two variables to evaluate each ECG:
            diagnosis = "normal" #if final diagnosis using all 19 variables marks ECG as normal/abnormal
            checklist = "normal" #if each individial variable marks ECG as normal/abnormal

            #Evaluation of diagnosis:
            counter = 0
            for variable in row[3:-1]:
                if int(variable) == 1:
                        counter +=1
            if counter != len(variables):
                diagnosis = "abnormal"

            #Evaluation of checklist:
            for checklistItem in possiblity[1]:
                if int(row[mapping[checklistItem]]) == 0:
                    checklist = "abnormal"

            # Abnormale som blir fanget opp
            if diagnosis == "abnormal" and checklist == "abnormal":
                possiblity[2] += 1

        #calculate percentage of abnormal ECG's that are catched by the combination
        possiblity[3] = possiblity[2] / numberOfAbnormal

    #Return list of results:
    results = [["number of variables","combination","#abnormale","%abnormale"]]
    for row in possibleChecklists:
        if row[3] > alfa:
            results.append(row)
    return(results)

def testChecklist(exportedChecklists, booleanChecklist, SCPcodes):
    #combine boolean checklist and SCP codes:
    ecgId = 1
    newChecklist = booleanChecklist
    for ecg in newChecklist[1:]:
        ecg.append(SCPcodes[ecgId][2])
        ecgId += 1

    #Get all checklistpointsvariables:
    checklistpoints = saveHeaderAsList(booleanChecklist)[3:]

    #link row in CSV to variable
    mapping = mappingColumn2Index(3,checklistpoints)

    #Dictionary with possible checklists:
    possibleChecklists = {}
    index = 1
    for possibleChecklist in exportedChecklists[1:]:
        #add space for specificity, sensitivty, NPV and PPV
        for i in range(8):
            possibleChecklist.append(0)
        possibleChecklists[index] = possibleChecklist
        index += 1

    #Check checklist against SCP and diagnostic info:
    for index,value in possibleChecklists.items():
        for row in newChecklist[1:]:
            #Set SCP diagnosis as normal (1) or abnormal (0)
            diagnosis = None
            if int(row[-1]) == 1:
                diagnosis = 1
            elif int(row[-1]) == 0:
                diagnosis = 0
            else:
                print(f'Diagnosis error!')

            checklist = 1
            for checklistpoint in value[1]:
                if int(row[int(mapping[checklistpoint])]) == 0:
                    checklist = 0

            if checklist and diagnosis:  # correct normal
                possibleChecklists[index][4] += 1
            elif checklist and not diagnosis:  # wrong normal
                possibleChecklists[index][5] += 1
            elif not checklist and diagnosis:  # wrong abnormal
                possibleChecklists[index][6] += 1
            elif not checklist and not diagnosis:  # true abnormal
                possibleChecklists[index][7] += 1
            else:
                print("error")

    #CALCULATE SENSITIVITE AND SPECIFICITy; PPV; NPV:
    ##possibleChecklists
    # 1 =sann normal (TN)
    # 2 =falsk normal (FN)
    # 3 =falsk abnormal (FP)
    # 4 =sann abnormal (TP)
    for key in possibleChecklists:
        TP = possibleChecklists[key][7]
        FP = possibleChecklists[key][6]
        FN = possibleChecklists[key][5]
        TN = possibleChecklists[key][4]

        possibleChecklists[key][8] = TP/(TP + FN)
        possibleChecklists[key][9] = TN / (TN + FP)
        possibleChecklists[key][10] = TP / (TP + FP)
        possibleChecklists[key][11] = TN / (TN + FN)

    export = [["combination", "True normal", "falsk normale", "falsk abnormal", "sann abnormal", "sensitivitet",
                    "spesifisitet", "PPV", "NPV"]]
    for index,value in possibleChecklists.items():
        export.append([value[0],value[4],value[5],value[6],value[7],round(value[8],5),round(value[9],5),round(value[10],5),round(value[11],5)])
    return(export)

#--------------------------
### LOGIC
#--------------------------

### INTER-INTERPRETATION VARIANCE
#read in individual checklists
age = readCSV("4_aages_checklist.csv")
vetle = readCSV("4_vetles_cheklist.csv")
#calculate variance
variance = variance_calculation(age, vetle)
#Export variance:
writeCSV("RESULT_variance.csv",variance)

### VARIABLES EFFECTING OUTPUT
numberOfPossibleVariables = 8
percentageOfUnormalECGToCatch = 0.95
#Read final checklist into python, select only necessary columns and normalize values to boolean 0/1
booleanChecklist = checklist_normalisation(checklist_cleanup(readCSV("3_combined_checklist.csv")))
#Retrieve checklistpoints from databse header
checklistpoints = extract_all_header_variables(booleanChecklist)
#Get all combinations of checklistpoints
possibleCombinations = possible_combinations(checklistpoints)

#### ANALYSE CHECKLIST USING ALL CHECKLISTCOMBINATIONS AND VARIABLES
ecgAnalysis = analyseChecklists(booleanChecklist,possibleCombinations,percentageOfUnormalECGToCatch)
writeCSV("RESULT_checklists.csv",ecgAnalysis)

#### TEST ALL CHECKLISTS AGAINST SCP CODES
SCPcodes = readCSV("5_scp_info.csv")
checklistTest = testChecklist(ecgAnalysis,booleanChecklist,SCPcodes)
writeCSV("RESULTS_SCP_comparison.csv",checklistTest)