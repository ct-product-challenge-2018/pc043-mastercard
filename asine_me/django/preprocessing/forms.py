from django import forms
from .objects import FeatureTypeChoice, DataTypeChoice

class UploadFileForm(forms.Form):
    checkbox = forms.BooleanField(
        label="I have read the above formatting rules and acknowledge the data I am uploading meets these "
              "requirements.")
    file = forms.FileField(label="Choose file to upload")

class PreprocessingDataForm(forms.Form):

    def __init__(self, *args, **kwargs):
        features = kwargs.pop('features')
        super(PreprocessingDataForm, self).__init__(*args, **kwargs)

        for feature in features:
            self.fields['%s_featureType' % feature] = forms.ChoiceField(
                label=feature,
                choices= [(choice.value, choice.value) for choice in FeatureTypeChoice])
            self.fields['%s_featureType' % feature].group = feature

            self.fields['%s_dataType' % feature] = forms.ChoiceField(
                label=feature,
                choices= [(choice.value, choice.value) for choice in DataTypeChoice])
            self.fields['%s_dataType' % feature].group = feature

    def features(self):
        for name, value in self.cleaned_data.items():
            yield (self.fields[name].label, value)
