from django import forms
from .objects import FieldTypeChoice

class NewLeadDynamicForm(forms.Form):

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields')
        super(NewLeadDynamicForm, self).__init__(*args, **kwargs)

        for field in fields:
            if field.type == FieldTypeChoice.CHAR_FIELD:
                self.fields[field.name] = forms.CharField(label=field.name)
            elif field.type == FieldTypeChoice.CHOICE_FIELD:
                self.fields[field.name] = forms.ChoiceField(label=field.name,
                                                               choices=[(choice,choice) for choice in field.categories])
            elif field.type == FieldTypeChoice.FLOAT_FIELD:
                self.fields[field.name] = forms.FloatField(label=field.name)

    def getFields(self):
        f = []
        for name, value in self.cleaned_data.items():
            f.append((self.fields[name].label, value))
        return f
