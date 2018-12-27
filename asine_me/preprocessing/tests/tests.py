from django.test import TestCase
from preprocessing.preprocessing_logic import getDfFromFile, getFeaturesFromDf, getUserInputFeatures, validateSalesData, PreprocessingFormField, validatePreprocessingInput
from preprocessing.messages import Messages
from preprocessing.forms import FeatureTypeChoice, DataTypeChoice
import os

class PreprocessingLogicTestCase(TestCase):
    def setUp(self):
        TEST_DATA_DIR = os.path.dirname(__file__) + "/testData/"
        self.INVALID_CSV_MISSING_REQUIRED_COLS = TEST_DATA_DIR + "invalid_csv_missingRequiredCols.csv"
        self.INVALID_CSV_ALL_PROBLEMS = TEST_DATA_DIR + "invalid_csv_missingCols_invalidSuccessValues_missingData.csv"
        self.INVALID_EXCEL_ALL_SUCCESSES = TEST_DATA_DIR + "invalid_excel_allSuccesses.xls"
        self.INVALID_EXCEL_INVALID_NUMERICAL_TEXT_FEATURE = TEST_DATA_DIR + "invalid_excel_invalidNumericalText.xlsx"
        self.INVALID_EXCEL_INVALID_NUMERICAL_NUMBER_FEATURE = TEST_DATA_DIR + "invalid_excel_invalidNumericalNumber.xlsx"
        self.INVALID_EXCEL_INVALID_BOOLEAN_TEXT_FEATURE = TEST_DATA_DIR + "invalid_excel_invalidBooleanText.xlsx"
        self.INVALID_EXCEL_INVALID_BOOLEAN_NUMBER_FEATURE = TEST_DATA_DIR + "invalid_excel_invalidBooleanNumber.xlsx"

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
            Messages.createEmptyCellsInColumnsMessage(['Referral', 'Opportunity Business Area'])]

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

    def testValidatePreprocessingInput_invalidNumericaText(self):
        df = getDfFromFile(self.INVALID_EXCEL_INVALID_NUMERICAL_TEXT_FEATURE)

        formField1 = PreprocessingFormField('NumericalNumber', FeatureTypeChoice.NUMERICAL.value, DataTypeChoice.NUMBER.value)
        formField2 = PreprocessingFormField('ValidNumericalText', FeatureTypeChoice.NUMERICAL.value, DataTypeChoice.TEXT.value)
        formField3 = PreprocessingFormField('InvalidNumericalText', FeatureTypeChoice.NUMERICAL.value, DataTypeChoice.TEXT.value)
        formFields = [formField1, formField2, formField3]

        expectedErrorMessages = [
            Messages.createInvalidNumericalFeatureTypeMessage(
                formField3.featureName, formField3.featureType, formField3.dataType)]

        # Test
        validPreprocessingInput, errorMessages = validatePreprocessingInput(formFields, df)

        # Validate
        self.assertEqual(validPreprocessingInput, False)

    def testValidatePreprocessingInput_invalidNumericalNumber(self):
        df = getDfFromFile(self.INVALID_EXCEL_INVALID_NUMERICAL_NUMBER_FEATURE)

        formField1 = PreprocessingFormField('ValidNumericalNumber', FeatureTypeChoice.NUMERICAL.value, DataTypeChoice.NUMBER.value)
        formField2 = PreprocessingFormField('InvalidNumericalNumber', FeatureTypeChoice.NUMERICAL.value, DataTypeChoice.NUMBER.value)
        formField3 = PreprocessingFormField('InvalidNumericalNumber2', FeatureTypeChoice.NUMERICAL.value, DataTypeChoice.NUMBER.value)
        formFields = [formField1, formField2, formField3]

        expectedErrorMessages = [
            Messages.createInvalidNumericalFeatureTypeMessage(
                formField2.featureName, formField2.featureType, formField2.dataType),
            Messages.createInvalidNumericalFeatureTypeMessage(
                formField3.featureName, formField3.featureType, formField3.dataType)
        ]

        # Test
        validPreprocessingInput, errorMessages = validatePreprocessingInput(formFields, df)

        # Validate
        self.assertEqual(validPreprocessingInput, False)
        self.assertEqual(errorMessages, expectedErrorMessages)

    def testValidatePreprocessingInput_invalidBooleanText(self):
        df = getDfFromFile(self.INVALID_EXCEL_INVALID_BOOLEAN_TEXT_FEATURE)

        formField1 = PreprocessingFormField('ValidBooleanText', FeatureTypeChoice.BOOLEAN.value, DataTypeChoice.TEXT.value)
        formField2 = PreprocessingFormField('ValidBooleanText2', FeatureTypeChoice.BOOLEAN.value, DataTypeChoice.TEXT.value)
        formField3 = PreprocessingFormField('ValidBooleanText3', FeatureTypeChoice.BOOLEAN.value, DataTypeChoice.TEXT.value)
        formField4 = PreprocessingFormField('InvalidBooleanText', FeatureTypeChoice.BOOLEAN.value, DataTypeChoice.TEXT.value)
        formFields = [formField1, formField2, formField3, formField4]

        expectedErrorMessages = [
            Messages.createInvalidBooleanFeatureTypeMessage(
                formField4.featureName, formField4.featureType, formField4.dataType),
        ]

        # Test
        validPreprocessingInput, errorMessages = validatePreprocessingInput(formFields, df)

        # Validate
        self.assertEqual(validPreprocessingInput, False)
        self.assertEqual(errorMessages, expectedErrorMessages)

    def testValidatePreprocessingInput_invalidBooleanNumber(self):
        df = getDfFromFile(self.INVALID_EXCEL_INVALID_BOOLEAN_NUMBER_FEATURE)

        formField1 = PreprocessingFormField('ValidBooleanNumber', FeatureTypeChoice.BOOLEAN.value, DataTypeChoice.NUMBER.value)
        formField2 = PreprocessingFormField('ValidBooleanNumber2', FeatureTypeChoice.BOOLEAN.value, DataTypeChoice.NUMBER.value)
        formField3 = PreprocessingFormField('ValidBooleanNumber3', FeatureTypeChoice.BOOLEAN.value, DataTypeChoice.NUMBER.value)
        formField4 = PreprocessingFormField('InvalidBooleanNumber', FeatureTypeChoice.BOOLEAN.value, DataTypeChoice.NUMBER.value)
        formFields = [formField1, formField2, formField3, formField4]

        expectedErrorMessages = [
            Messages.createInvalidBooleanFeatureTypeMessage(
                formField4.featureName, formField4.featureType, formField4.dataType),
        ]

        # Test
        validPreprocessingInput, errorMessages = validatePreprocessingInput(formFields, df)

        # Validate
        self.assertEqual(validPreprocessingInput, False)
        self.assertEqual(errorMessages, expectedErrorMessages)