import numpy as np
from sklearn.externals import joblib
from preprocessing.objects import MODEL_FILENAME, SCALER_FILENAME, FeatureTypeChoice
from .objects import NewLeadFormField

# Input new leads functions --------------------------------------------------------------------------------------------
def getInputNewLeadFields(clientColHeader, userInputFeatures, preprocessingSteps):
    fields = []
    clientIdField = NewLeadFormField(clientColHeader)
    clientIdField.setAsCharField()
    fields.append(clientIdField)

    for feature in userInputFeatures:
        field = NewLeadFormField(feature)
        preprocessingStep = preprocessingSteps[feature]

        if preprocessingStep.formField.featureType == FeatureTypeChoice.CATEGORICAL.value \
                or preprocessingStep.formField.featureType == FeatureTypeChoice.BOOLEAN.value:
            field.setAsChoiceField(preprocessingStep.categories)
        elif preprocessingStep.formField.featureType == FeatureTypeChoice.NUMERICAL.value:
            field.setAsFloatField()

        fields.append(field)

    return fields

# Recommendations functions --------------------------------------------------------------------------------------------
def loadObjectFromFile(filePath):
    return joblib.load(filePath)

def getMatchingDynamicRecommendationsContext(fields,
                                             userInputFeatures,
                                             featureNameMapping,
                                             preprocessingSteps,
                                             featureCols):
    numFeatures = len(featureCols)

    # Feature vector for new lead
    featureVector = np.zeros(numFeatures)

    for feature in userInputFeatures:
        if preprocessingSteps[feature].codingMap != None:
            coding = preprocessingSteps[feature].codingMap
            offset = featureCols.index(feature)
            featureVector[offset] = coding.get(fields[feature])
        elif preprocessingSteps[feature].dummyCols != None:
            dummyCols = preprocessingSteps[feature].dummyCols
            offset = featureCols.index(dummyCols[0])
            for i in range(offset, offset+len(dummyCols)):
                colName = featureCols[i]
                if colName.endswith(fields[feature]):
                    featureVector[i] = 1
        else:
            offset = featureCols.index(feature)
            featureVector[offset] = float(fields[feature])

    # Dummy columns for categorical features
    salespeopleColHeader = featureNameMapping['salesperson id']
    salesPersonDummyColumns = preprocessingSteps[salespeopleColHeader].dummyCols
    salesPersonDummyColumnsOffset = featureCols.index(salesPersonDummyColumns[0])

    # Classifier
    log_reg = loadObjectFromFile(MODEL_FILENAME)
    scaler = loadObjectFromFile(SCALER_FILENAME)

    top_ten = getMatchProbabilities(
        log_reg,
        scaler,
        featureVector,
        salesPersonDummyColumnsOffset,
        salesPersonDummyColumns)

    context = {
        'clientName': fields[featureNameMapping['client id']],
        'numSalespeople': len(salesPersonDummyColumns),
        'featureVector': featureVector,
        'fields': fields,
        'top_ten': top_ten
    }

    return context

def getMatchProbabilities(classifier, scaler, featureVector, salesPersonDummyColumnsOffset, salesPersonDummyColumns):
    recommended_salespeople = [] # Records salespeople and probability
    for i in range(len(salesPersonDummyColumns)):
        # Reshape so that the feature vector is a row in a matrix
        X_test_sales_person_row = featureVector.reshape(1,-1).copy()

        # Set salesperson bit
        X_test_sales_person_row[0][salesPersonDummyColumnsOffset+i] = 1

        X_test_sales_person_row = scaler.transform(X_test_sales_person_row)

        # Get probability of success
        prob = classifier.predict_proba(X_test_sales_person_row)[0][1]

        base_location = "../../static/recommendations/icons/"
        if prob > 0.7:
            recommended_salespeople.append([salesPersonDummyColumns[i], prob, base_location + "Full.png", "70% to 100%"])
        elif prob > 0.5:
            recommended_salespeople.append([salesPersonDummyColumns[i], prob, base_location + "Half.png", "50% to 70%"])
        else:
            recommended_salespeople.append([salesPersonDummyColumns[i], prob, base_location + "Empty.png", "Less than 50%"])

        # Clear salesperson bit
        X_test_sales_person_row[0][salesPersonDummyColumnsOffset+i] = 0

    # Find top 10 salespeople by probability of success
    recommended_salespeople = np.array(recommended_salespeople)
    recommended_salespeople = recommended_salespeople[np.argsort(recommended_salespeople[:, 1])]
    top_ten = recommended_salespeople[-10:,:][::-1]
    top_ten = top_ten[:,[0,2,3]].tolist()

    return top_ten
