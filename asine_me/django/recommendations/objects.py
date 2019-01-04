from enum import Enum

class FieldTypeChoice(Enum):
    CHAR_FIELD = "CharField"
    CHOICE_FIELD = "ChoiceField"
    FLOAT_FIELD = "FloatField"

class NewLeadFormField:
    def __init__(self, featureName):
        self.name = featureName
        self.type = None
        self.categories = None

    def setAsCharField(self):
        self.type = FieldTypeChoice.CHAR_FIELD

    def setAsChoiceField(self, categories):
        self.type = FieldTypeChoice.CHOICE_FIELD
        self.categories = categories

    def setAsFloatField(self):
        self.type = FieldTypeChoice.FLOAT_FIELD