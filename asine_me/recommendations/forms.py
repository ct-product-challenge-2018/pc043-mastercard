from django import forms

class NewLeadForm(forms.Form):
    clientName = forms.CharField(label="Account Name", required=True)

    vertical = forms.ChoiceField(
        label="Opportunity Business Area",
        choices=[("Legal", "Legal"), #eCommerce Business
                 ("Education", "Education"), #Payment Terminal Business
                 ("Health", "Health"), #POS Acquiring
                 ("Not Applicable", "Not Applicable"),])

    salesPersonReferral = forms.ChoiceField(
        label = "Referred",
        choices=[("True","True"),
                 ("False","False"),
                 ("Not Applicable", "Not Applicable")])

    salesProcess = forms.ChoiceField(
        label="Opportunity Sales Process",
        choices=[("New Business", "New Business"),
                 ("Upsell", "Upsell")])

class NewLeadDynamicForm(forms.Form):

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields')
        super(NewLeadDynamicForm, self).__init__(*args, **kwargs)

        #fieldInf is a list of [label, type, choices]
        for field in fields:
            if field['type'] == "CharField":
                self.fields[field['name']] = forms.CharField(label=field['name'])
            else:
                self.fields[field['name']] = forms.ChoiceField(label=field['name'],
                                                               choices=[(choice,choice) for choice in field['categories']])

    def getFields(self):
        f = []
        for name, value in self.cleaned_data.items():
            f.append((self.fields[name].label, value))
        return f
