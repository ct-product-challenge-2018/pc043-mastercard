import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.externals import joblib
from .messages import Messages

import numpy as np

class InvalidInput(Exception):
    pass

def getDfFromFile(file):
    try:
        df = pd.read_csv(file)
        return df
    except:
        try:
            df = pd.read_excel(file)
            return df
        except:
            raise InvalidInput(Messages.INVALID_SALES_DATA_FILE_TYPE)


#TODO: better header cleaning to remove punctuation, spaces, etc.
def getFeaturesFromDf(df):
    featuresList = [] # Gives the order of the lowercase feature names in the dataframe
    featureNameMapping = {} # Gives the mapping from lowercase to original name for column headers

    for col in df.columns:
        lowercaseCol = col.lower()
        featuresList.append(lowercaseCol)
        featureNameMapping[lowercaseCol] = col

    return featuresList, featureNameMapping


def getUserInputFeatures(features, featureNameMapping):
    return [featureNameMapping[f] for f in features if (f != "client id" and f != 'salesperson id' and f != 'success')]


def getDataframeFromJson(jsonData):
    return pd.read_json(jsonData)


def getCategoriesAndCounts(df, colHeader):
    counts = df[colHeader].value_counts()
    categories = sorted(counts.index.tolist())
    return categories, counts


# createModel helper functions
def getJsonDataframe(df):
    return df.to_json()


#TODO: better validation such as duplicate column names, etc.
#TODO: give users options for handling empty cells
def validateSalesData(features, featureNameMapping, df):
    errorMessages = []
    valid = True

    # Validate all required columns are present
    if("client id" not in features):
        valid = False
        errorMessages.append(Messages.MISSING_CLIENT_ID_COLUMN)

    if('success' not in features):
        valid = False
        errorMessages.append(Messages.MISSING_SALESPERSON_ID_COLUMN)

    if('salesperson id' not in features):
        valid = False
        errorMessages.append(Messages.MISSING_SUCCESS_COLUMN)

    # Validate success column
    if('success' in featureNameMapping.keys()):
        successColHeader = featureNameMapping['success']
        # We assume that the larger value is 'success', and the smaller value is 'failure'
        successValues, successValueCounts = getCategoriesAndCounts(df, successColHeader)
        if(len(successValues) != 2):
            valid = False
            errorMessages.append(Messages.INVALID_SUCCESS_VALUES)

    # Validate there are no empty cells
    colsWithEmptyCells = df.columns[df.isna().any()].tolist()
    if(len(colsWithEmptyCells) > 0):
        valid = False
        errorMessages.append(Messages.createEmptyCellsInColumnsMessages(colsWithEmptyCells))

    return valid, errorMessages


# dataPreprocessing helper functions
def buildModel(df, successColHeader, clientColHeader):
    # Separate labels
    modified_df = df.copy()
    y = modified_df[successColHeader].as_matrix()
    modified_df = modified_df.drop([successColHeader], axis=1)
    modified_df = modified_df.drop([clientColHeader], axis=1)
    X = modified_df.as_matrix()

    X_train, X_test, y_train, y_test = train_test_split(X,y, test_size = 0.2, random_state = 1)
    modelFilename = 'recommendations/static/recommendations/session_model.joblib'

    # Train the model
    log_reg = LogisticRegression().fit(X_train,y_train)

    # Write the model to a file
    joblib.dump(log_reg, modelFilename)

    return log_reg.score(X_test, y_test), modified_df.columns.tolist()


def preprocessDf(df, successColHeader, salespeopleColHeader, clientsColHeader, formFields):
    np.random.seed(0)
    modified_df = df.copy()

    preprocessingSteps = {}

    for formField in formFields:
        colHeader = formField['name']
        if formField['featureType'] == 'Categorical':
            categories, categoryCounts = getCategoriesAndCounts(df, colHeader)
            if(len(categories) > 2):
                modified_df, dummyCols = convertCategoricalToDummies(modified_df, colHeader)
                preprocessingSteps[colHeader] ={
                    'name': colHeader,
                    'formField':formField,
                    'categories': categories,
                    'dummyCols': dummyCols
                }
            elif(len(categories) == 2):
                codingMap = {}
                i = 0
                for category in categories:
                    codingMap[category] = i
                    i +=1
                modified_df[colHeader] = modified_df[colHeader].replace(codingMap)
                preprocessingSteps[colHeader] ={
                    'name': colHeader,
                    'formField':formField,
                    'categories': categories,
                    'coding': codingMap
                }
            else: # If there is less than 2 categories, it is not useful
                modified_df = convertedDf.drop([colHeader], axis=1)
        elif formField['featureType'] == 'Boolean':
            categories, categoryCounts = getCategoriesAndCounts(df, colHeader)
            if(formField['dataType']== "Number"):
                preprocessingSteps[colHeader] ={
                    'name': colHeader,
                    'formField':formField,
                    'categories': categories,
                }
        #elif formField['featureType'] == 'Numerical':
            # TODO handle this

    #Salespeople
    salespeopleIds, salespeopleIdCounts = getCategoriesAndCounts(modified_df, salespeopleColHeader)
    modified_df, dummyCols = convertCategoricalToDummies(modified_df, salespeopleColHeader)
    preprocessingSteps[salespeopleColHeader] = {
        'name': salespeopleColHeader,
        'formField': formField,
        'categories': salespeopleIds,
        'dummyCols': dummyCols
    }

    return modified_df, preprocessingSteps


def convertCategoricalToDummies(df, colHeader):
    convertedDf = df.copy()
    columns_to_drop = []

    dummies = pd.get_dummies(convertedDf[colHeader])

    new_column_names = []
    for j in range(len(dummies.columns)):
        new_column_names.append(colHeader + "_" + str(dummies.columns[j]))

    dummies.columns = new_column_names
    columns_to_drop.append(colHeader)

    convertedDf = pd.concat([convertedDf, dummies], axis=1)
    convertedDf = convertedDf.drop(columns_to_drop, axis=1)
    return convertedDf, dummies.columns.tolist()


def convertCategoricalToCodes(df, colHeader):
    convertedDf = df.copy()
    codingMap = {}
    i = 0
    for category in categories:
        codingMap[category] = i
        i += 1
    convertedDf[colHeader] = convertedDf[colHeader].replace(codingMap)
    return convertedDf, codingMap

