import numpy as np
from sklearn.externals import joblib

# Helper functions
def loadClassifier(model_path):
    return joblib.load(model_path)

def codeCategoricalField(value, sales_process_dict):
    return sales_process_dict.get(value)

def getMatchingDynamicRecommendationsContext(fields,
                                             userInputFeatures,
                                             featureNameMapping,
                                             preprocessingSteps,
                                             featureCols):
    numFeatures = len(featureCols)
    # Feature vector for new lead
    featureVector = np.zeros(numFeatures)

    for feature in userInputFeatures:
        if 'coding' in preprocessingSteps[feature].keys():
            coding = preprocessingSteps[feature]['coding']
            offset = featureCols.index(feature)
            featureVector[offset] = codeCategoricalField(fields[feature], coding)
        elif 'dummyCols' in preprocessingSteps[feature].keys():
            dummyCols = preprocessingSteps[feature]['dummyCols']
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
    salesPersonDummyColumns = preprocessingSteps[salespeopleColHeader]['dummyCols']
    salesPersonDummyColumnsOffset = featureCols.index(salesPersonDummyColumns[0])

    # Classifier
    log_reg = loadClassifier('recommendations/static/recommendations/session_model.joblib')

    top_ten = getMatchProbabilities(
        log_reg,
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


def getMatchProbabilities(classifier, featureVector, salesPersonDummyColumnsOffset, dummies_columns):
    recommended_salespeople = [] # Records salespeople and probability
    for i in range(len(dummies_columns)):
        X_test_sales_person_row = featureVector.reshape(1,-1)

        # Set salesperson bit
        X_test_sales_person_row[0][salesPersonDummyColumnsOffset+i] = 1

        X_test_sales_person_row = featureVector.reshape(1,-1)
        prob = classifier.predict_proba(X_test_sales_person_row)[0][1]
        base_location = "../../static/recommendations/icons/"
        if prob > 0.7:
            recommended_salespeople.append([dummies_columns[i], prob, base_location + "Full.png", "70% to 100%"])
        elif prob > 0.5:
            recommended_salespeople.append([dummies_columns[i], prob, base_location + "Half.png", "50% to 70%"])
        else:
            recommended_salespeople.append([dummies_columns[i], prob, base_location + "Empty.png", "Less than 50%"])

        # Clear salesperson bit
        X_test_sales_person_row[0][salesPersonDummyColumnsOffset+i] = 0

    # Find top 10 salespeople by probability of success
    recommended_salespeople = np.array(recommended_salespeople)
    recommended_salespeople = recommended_salespeople[np.argsort(recommended_salespeople[:, 1])]
    top_ten = recommended_salespeople[-10:,:][::-1]
    top_ten = top_ten[:,[0,2,3]].tolist()

    return top_ten
