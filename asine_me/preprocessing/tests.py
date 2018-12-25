from django.test import TestCase
from .preprocessing_logic import getDfFromFile, getFeaturesFromDf, getUserInputFeatures
import os

class PreprocessingLogicTestCase(TestCase):
    def setUp(self):
        TEST_DATA_DIR = os.path.dirname(__file__) + "/tests/testData/"
        self.INVALID_CSV_MISSING_REQUIRED_COLS = TEST_DATA_DIR + "invalid_csv_noSuccessCol.csv"
        self.INVALID_CSV_ALL_PROBLEMS = TEST_DATA_DIR + "invalid_csv_missingCols_invalidSuccessValues_missingData.csv"

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
