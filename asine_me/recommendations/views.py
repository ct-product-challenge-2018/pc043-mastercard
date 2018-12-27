from django.shortcuts import render, redirect
from django.contrib import messages
from preprocessing.preprocessing_logic import getUserInputFeatures
from preprocessing.messages import Messages as PreprocessingMessages
from preprocessing.objects import as_PreprocessingStep
from .forms import NewLeadDynamicForm
from .matching_logic import getInputNewLeadFields, getMatchingDynamicRecommendationsContext
import json

def inputNewLeads(request):
    if ('featuresList' in request.session
            and 'featureNameMapping' in request.session
            and 'preprocessingSteps' in request.session
            and 'modifiedDfFeatureCols' in request.session):
        featuresList = request.session['featuresList']
        featureNameMapping = request.session['featureNameMapping']
        userInputFeatures = getUserInputFeatures(featuresList, featureNameMapping)
        preprocessingSteps = {k: as_PreprocessingStep(json.loads(v)) for k, v in request.session['preprocessingSteps'].items()}

        clientColHeader = featureNameMapping['client id']
        fields = getInputNewLeadFields(clientColHeader, userInputFeatures, preprocessingSteps)

        if request.method == "POST":
            form = NewLeadDynamicForm(request.POST, fields=fields)
            if form.is_valid():
                request.session['newLeadFields'] = form.cleaned_data
                return redirect('recommendations')
        else:
            form = NewLeadDynamicForm(fields = fields)

        context = {
            'form': form,
        }
        return render(request, 'recommendations/input_new_leads.html', context)

    messages.warning(request, PreprocessingMessages.MISSING_SALES_DATA)
    return redirect('create_model')

def recommendations(request):
    if ('newLeadFields' in request.session
            and 'featuresList' in request.session
            and 'featureNameMapping' in request.session
            and 'preprocessingSteps' in request.session
            and 'modifiedDfFeatureCols' in request.session):
        newLeadFields = request.session['newLeadFields']
        featuresList = request.session['featuresList']
        featureNameMapping = request.session['featureNameMapping']
        userInputFeatures = getUserInputFeatures(featuresList, featureNameMapping)
        preprocessingSteps = {k: as_PreprocessingStep(json.loads(v)) for k, v in request.session['preprocessingSteps'].items()}
        modifiedDfFeatureCols = request.session['modifiedDfFeatureCols']

        context = getMatchingDynamicRecommendationsContext(newLeadFields, userInputFeatures, featureNameMapping, preprocessingSteps, modifiedDfFeatureCols)
        return render(request, 'recommendations/recommendations.html', context)

    messages.warning(request, PreprocessingMessages.MISSING_SALES_DATA)
    return redirect('create_model')