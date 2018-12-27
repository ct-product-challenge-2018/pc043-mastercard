# Error messages shown in the UI
class Messages:
    MISSING_SALES_DATA = "Please upload a sales data file and acknowledge the formatting rules first."
    INVALID_SALES_DATA_FILE_TYPE = "Please upload an excel or csv file."

    MISSING_CLIENT_ID_COLUMN = "Please make sure there is a 'Client ID' column in the sales data."
    MISSING_SALESPERSON_ID_COLUMN = "Please make sure there is a 'Salesperson ID' column in the sales data."
    MISSING_SUCCESS_COLUMN = "Please make sure there is a 'Success' column in the sales data."
    INVALID_SUCCESS_VALUES = "Please make sure the 'Success' column has 1s and 0s as values."

    @staticmethod
    def createEmptyCellsInColumnsMessage(colsWithEmptyCells):
        return "The following columns contain empty cells: {}".format(', '.join(colsWithEmptyCells))

    @staticmethod
    def createUncaughtCaseMessage(uncaughtCase):
        return "The following case is not yet handled: {}. Please contact us for assistance.".format(uncaughtCase)

    @staticmethod
    def createInvalidNumericalFeatureTypeMessage(featureName, featureType, dataType):
        return "{} is not a valid {} {} column. Please check the data.".format(featureName, featureType, dataType)

    @staticmethod
    def createInvalidBooleanFeatureTypeMessage(featureName, featureType, dataType):
        return "{} is not a valid {} {} column. Please check that there are at most two types of values (true and false) for this column.".format(featureName, featureType, dataType)