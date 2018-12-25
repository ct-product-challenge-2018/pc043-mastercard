class Messages():
    INVALID_SALES_DATA_FILE_TYPE = "Please upload an excel or csv file."
    MISSING_CLIENT_ID_COLUMN = "Please make sure there is a 'Client ID' column in the sales data."
    MISSING_SALESPERSON_ID_COLUMN = "Please make sure there is a 'Salesperson ID' column in the sales data."
    MISSING_SUCCESS_COLUMN = "Please make sure there is a 'Success' column in the sales data."
    INVALID_SUCCESS_VALUES = "Please make sure the 'Success' column has 1s and 0s as values."

    @staticmethod
    def createEmptyCellsInColumnsMessages(colsWithEmptyCells):
        return "The following columns contain empty cells: {}".format(', '.join(colsWithEmptyCells))