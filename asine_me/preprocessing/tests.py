from django.test import TestCase
from .preprocessing_logic import getUserInputFeatures

class PreprocessingLogicTestCase(TestCase):
    def testGetUserInputFeatures(self):
        featureNameMapping = {
            'client id': 'Client ID',
            'referral': 'Referral',
            'sales process': 'Sales Process',
            'opportunity business area': 'Opportunity Business Area',
            'salesperson id': 'Salesperson ID',
            'success': 'Success',
        }
        inputFeatures = getUserInputFeatures(featureNameMapping.keys(), featureNameMapping)

        expectedInputFeatures = ['Referral', 'Sales Process', 'Opportunity Business Area']
        self.assertEqual(inputFeatures, expectedInputFeatures)
