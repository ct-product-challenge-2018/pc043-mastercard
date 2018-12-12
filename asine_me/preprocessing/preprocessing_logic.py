import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.externals import joblib
import json

import numpy as np

def getFeatures(file):
    df = pd.read_excel(file)
    featuresList = [] # Gives the order of the features in the dataframe
    featureNameMapping = {} # Gives the mapping from lowercase to original name for column headers

    for col in df.columns:
        lowercaseCol = col.lower()
        featuresList.append(lowercaseCol)
        featureNameMapping[lowercaseCol] = col
    #TODO: better header cleaning to remove punctuation, spaces, etc.

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
def getJsonDataframe(file):
    #TODO: handle csv files
    return pd.read_excel(file).to_json()

def validateSalesData(features, featureNameMapping, df):
    errorMessages = []
    valid = True
    if("client id" not in features):
        valid = False
        errorMessages.append("Please make sure there is a 'Client ID' column in the sales data")

    if('success' not in features):
        valid = False
        errorMessages.append("Please make sure there is a 'Success' column in the sales data")

    if('salesperson id' not in features):
        valid = False
        errorMessages.append("Please make sure there is a 'Salesperson ID' column in the sales data")

    return valid, errorMessages

    # Validate success column
    successColHeader = featureNameMapping['success']
    # We assume that the larger value is 'success', and the smaller value is 'failure'
    successValues, successValueCounts = getCategoriesAndCounts(df, successColHeader)
    if(len(successValues) != 2):
        valid = False
        errorMessages.append("Please make sure the 'Success' column has only 1s and 0s as values.")

    #TODO: better validation such as duplicate column names, etc.

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
        'formField':formField,
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
        i +=1
    convertedDf[colHeader] = convertedDf[colHeader].replace(codingMap)
    return convertedDf, codingMap
