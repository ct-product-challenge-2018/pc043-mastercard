from django.shortcuts import render, redirect
from .forms import NewLeadForm, NewLeadDynamicForm
from django.contrib import messages
from .matching_logic import getMatchingDynamicRecommendationsContext
from preprocessing.preprocessing_logic import getUserInputFeatures

def home(request):
    return render(request, 'recommendations/home.html')

def welcome(request):
    return render(request, 'recommendations/welcome.html')

def recommendations(request):
    if ('fields' in request.session
        and 'featuresList' in request.session
        and 'featureNameMapping' in request.session
        and 'preprocessingSteps' in request.session
        and 'featureCols' in request.session):
        fields = request.session['fields']
        featuresList = request.session['featuresList']
        featureNameMapping = request.session['featureNameMapping']
        userInputFeatures = getUserInputFeatures(featuresList, featureNameMapping)
        preprocessingSteps = request.session['preprocessingSteps']
        featureCols = request.session['featureCols']

        context = getMatchingDynamicRecommendationsContext(fields, userInputFeatures, featureNameMapping, preprocessingSteps, featureCols)
        return render(request, 'recommendations/recommendations.html', context)

    messages.warning(request, f'Please upload a sales data file and acknowledge the formatting rules first.')
    return redirect('create_model')

def inputNewLeads(request):
    if ('featuresList' in request.session
            and 'featureNameMapping' in request.session
            and 'preprocessingSteps' in request.session
            and 'featureCols' in request.session):
        featuresList = request.session['featuresList']
        featureNameMapping = request.session['featureNameMapping']
        userInputFeatures = getUserInputFeatures(featuresList, featureNameMapping)
        preprocessingSteps = request.session['preprocessingSteps']

        fields = []
        fields.append({
            'name': featureNameMapping['client id'],
            'type': 'CharField'
        })

        for feature in userInputFeatures:
            field = {}
            formField = preprocessingSteps[feature]['formField']

            field['name'] = feature
            if formField['featureType'] == 'Categorical' or formField['featureType']  == 'Boolean':
                field['type'] = 'ChoiceField'
                field['categories'] = preprocessingSteps[feature]['categories']
            #elif formField.featureType == 'Numerical':
                #TODO handle this

            fields.append(field)

        if request.method == "POST":
            form = NewLeadDynamicForm(request.POST, fields = fields)
            if form.is_valid():
                request.session['fields'] = form.cleaned_data
                return redirect('recommendations')
        else:
            form = NewLeadDynamicForm(fields = fields)

        context = {
            'form': form,
        }
        return render(request, 'recommendations/input_new_leads.html', context)

    messages.warning(request, f'Please upload a sales data file and acknowledge the formatting rules first.')
    return redirect('create_model')