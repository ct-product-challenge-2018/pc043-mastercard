from django.test import TestCase
from preprocessing.preprocessing_logic import getDfFromFile, getFeaturesFromDf, getUserInputFeatures, validateSalesData
from preprocessing.messages import Messages
import os

class PreprocessingLogicTestCase(TestCase):
    def setUp(self):
        TEST_DATA_DIR = os.path.dirname(__file__) + "/testData/"
        self.INVALID_CSV_MISSING_REQUIRED_COLS = TEST_DATA_DIR + "invalid_csv_missingRequiredCols.csv"
        self.INVALID_CSV_ALL_PROBLEMS = TEST_DATA_DIR + "invalid_csv_missingCols_invalidSuccessValues_missingData.csv"
        self.INVALID_EXCEL_ALL_SUCCESSES = TEST_DATA_DIR + "invalid_excel_allSuccesses.xls"

    def testGetFeaturesFromDf(self):
        df = getDfFromFile(self.INVALID_CSV_ALL_PROBLEMS)
        expectedFeatureNameMapping = {
            'client ids': 'Client IDs',
            'referral': 'Referral',
            'sales process': 'Sales Process',
            'opportunity business area': 'Opportunity Business Area',
            'salesperson id': 'Salesperson ID',
            'success': 'Success',
        }
        expectedInputFeatures = ['client ids', 'referral', 'sales process',
                                 'opportunity business area', 'salesperson id', 'success']

        # Test
        featuresList, featureNameMapping = getFeaturesFromDf(df)

        # Validate
        self.assertEqual(featuresList, expectedInputFeatures)
        self.assertEqual(featureNameMapping, expectedFeatureNameMapping)

    def testGetUserInputFeatures(self):
        featureNameMapping = {
            'client id': 'Client ID',
            'referral': 'Referral',
            'sales process': 'Sales Process',
            'opportunity business area': 'Opportunity Business Area',
            'salesperson id': 'Salesperson ID',
            'success': 'Success',
        }
        expectedInputFeatures = ['Referral', 'Sales Process', 'Opportunity Business Area']

        # Test
        inputFeatures = getUserInputFeatures(featureNameMapping.keys(), featureNameMapping)

        # Validate
        self.assertEqual(inputFeatures, expectedInputFeatures)

    def testValidateSalesData_missingRequiredCols(self):
        df = getDfFromFile(self.INVALID_CSV_MISSING_REQUIRED_COLS)
        featuresList, featureNameMapping = getFeaturesFromDf(df)

        expectedErrorMessages = [
            Messages.MISSING_CLIENT_ID_COLUMN,
            Messages.MISSING_SALESPERSON_ID_COLUMN,
            Messages.MISSING_SUCCESS_COLUMN]

        # Test
        validSalesData, errorMessages = validateSalesData(featuresList,
                                                          featureNameMapping,
                                                          df)
        # Validate
        self.assertEqual(validSalesData, False)
        self.assertEqual(errorMessages, expectedErrorMessages)

    def testValidateSalesData_allProblems(self):
        df = getDfFromFile(self.INVALID_CSV_ALL_PROBLEMS)
        featuresList, featureNameMapping = getFeaturesFromDf(df)

        expectedErrorMessages = [
            Messages.MISSING_CLIENT_ID_COLUMN,
            Messages.INVALID_SUCCESS_VALUES,
            Messages.createEmptyCellsInColumnsMessages(['Referral', 'Opportunity Business Area'])]

        # Test
        validSalesData, errorMessages = validateSalesData(featuresList,
                                                          featureNameMapping,
                                                          df)
        # Validate
        self.assertEqual(validSalesData, False)
        self.assertEqual(errorMessages, expectedErrorMessages)

    def testValidateSalesData_allSuccesses(self):
        df = getDfFromFile(self.INVALID_EXCEL_ALL_SUCCESSES)
        featuresList, featureNameMapping = getFeaturesFromDf(df)

        expectedErrorMessages = [
            Messages.INVALID_SUCCESS_VALUES]

        # Test
        validSalesData, errorMessages = validateSalesData(featuresList,
                                                          featureNameMapping,
                                                          df)
        # Validate
        self.assertEqual(validSalesData, False)
        self.assertEqual(errorMessages, expectedErrorMessages)