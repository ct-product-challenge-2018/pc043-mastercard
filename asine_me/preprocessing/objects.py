from enum import Enum
import json

MODEL_FILENAME = 'recommendations/static/recommendations/session_model.joblib'
SCALER_FILENAME = 'recommendations/static/recommendations/session_scaler.joblib'

class FeatureTypeChoice(Enum):
    CATEGORICAL = "Categorical"
    NUMERICAL = "Numerical"
    BOOLEAN = "Boolean"

class DataTypeChoice(Enum):
    TEXT = "Text"
    NUMBER = "Number"

class InvalidInput(Exception):
    pass

class UncaughtCase(Exception):
    pass

class PreprocessingFormField:
    def __init__(self, featureName, featureType, dataType):
        self.featureName = featureName
        self.featureType = featureType
        self.dataType = dataType

    def to_JSON(self):
        # Dumps the JSON correctly, passing over the __dict__ of the class to assmble it.
        return json.dumps(self, default=lambda o: o.__dict__)

def as_PreprocessingFormField(json):
    return PreprocessingFormField(json['featureName'], json['featureType'], json['dataType'])

class PreprocessingConfirmation:
    def __init__(self, formField):
        self.formField = formField

        # Categorical or Boolean feature fields
        self.uniqueCategories = None

        # Numerical feature field
        self.min = None
        self.max = None

    def setCategoricalOrBooleanFeatureFields(self, uniqueCategories):
        self.uniqueCategories = uniqueCategories
        self.numUniqueCategories = len(uniqueCategories)

    def setNumericalFeatureFields(self, min, max):
        self.min = min
        self.max = max

    def isCategoricalOrBoolean(self):
        return (self.formField.featureType == FeatureTypeChoice.CATEGORICAL.value
                or self.formField.featureType == FeatureTypeChoice.BOOLEAN.value)

    def isNumerical(self):
        return self.formField.featureType == FeatureTypeChoice.NUMERICAL.value

class PreprocessingStep:
    def __init__(self, featureName, formField):
        self.featureName = featureName
        self.formField = formField

        # Categorical or Boolean feature fields
        self.categories = None
        # Binary categorical or boolean features
        self.codingMap = None
        # Categorical features with more than two classes
        self.dummyCols = None

        # No Numerical feature fields needed. We will use a scaler over the data.

    def setBinaryCategoricalOrBooleanFeatureFields(self, categories, codingMap):
        self.categories = categories
        self.codingMap = codingMap

    def setCategoricalFeatureFields(self, categories, dummyCols):
        self.categories = categories
        self.dummyCols = dummyCols

    def isCategoricalOrBoolean(self):
        return (self.formField.featureType == FeatureTypeChoice.CATEGORICAL.value
                or self.formField.featureType == FeatureTypeChoice.BOOLEAN.value)

    def isNumerical(self):
        return self.formField.featureType == FeatureTypeChoice.NUMERICAL.value

    def to_JSON(self):
        # Dumps the JSON correctly, passing over the __dict__ of the class to assmble it.
        return json.dumps(self, default=lambda o: o.__dict__)

def as_PreprocessingStep(json):
    formField = as_PreprocessingFormField(json['formField'])
    preprocessingStep = PreprocessingStep(json['featureName'], formField)
    if preprocessingStep.formField.featureType == FeatureTypeChoice.CATEGORICAL.value:
        categories = json['categories']
        if(json['dummyCols'] != None): # The salesperson ids will always use dummy columns
            dummyCols = json['dummyCols']
            preprocessingStep.setCategoricalFeatureFields(categories, dummyCols)
        else:
            codingMap = json['codingMap']
            preprocessingStep.setBinaryCategoricalOrBooleanFeatureFields(categories,codingMap)
    elif preprocessingStep.formField.featureType == FeatureTypeChoice.BOOLEAN.value:
        categories = json['categories']
        codingMap = json['codingMap']
        preprocessingStep.setBinaryCategoricalOrBooleanFeatureFields(categories,codingMap)
    elif formField.featureType == FeatureTypeChoice.NUMERICAL.value:
        # We will use a scaler for the numerical columns in buildModel
        pass
    else:
        raise UncaughtCase(Messages.createUncaughtCaseMessage("Feature type '{}'".format(formField.featureType)))

    return preprocessingStep