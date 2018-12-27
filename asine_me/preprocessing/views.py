from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UploadFileForm, PreprocessingDataForm
from .preprocessing_logic import getDfFromFile, getFeaturesFromDf, getJsonDataframe, preprocessDf, validateSalesData, \
    getUserInputFeatures, validatePreprocessingInput, getDataframeFromJson, getCategoriesAndCounts, buildModel, \
    getUserInputFieldConfirmations
from .messages import Messages
from .objects import PreprocessingFormField, as_PreprocessingFormField
import json

def createModel(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid() and form.cleaned_data.get('checkbox') == True:
            try:
                df = getDfFromFile(request.FILES['file'])
                featuresList, featureNameMapping = getFeaturesFromDf(df)

                # Validate sales data follows formatting rules
                validSalesData, errorMessages = validateSalesData(featuresList,
                                                                  featureNameMapping,
                                                                  df)
                if not validSalesData:
                    for errorMessage in errorMessages:
                        messages.warning(request, errorMessage)
                    return redirect('create_model')

                # Set session variables and redirect to next step
                request.session['dataframe'] = getJsonDataframe(df)
                request.session['featuresList'] = featuresList
                request.session['featureNameMapping'] = featureNameMapping
                return redirect('data_preprocessing')
            except Exception as e:
                messages.warning(request, e)
    else:
        form = UploadFileForm()

    request.session.flush()
    context = {
        'form': form,
    }
    return render(request, 'preprocessing/create_model.html', context)

def dataPreprocessing(request):
    if ('featuresList' in request.session
            and 'featureNameMapping' in request.session
            and 'dataframe' in request.session):
        featuresList = request.session['featuresList']
        featureNameMapping = request.session['featureNameMapping']
        userInputFeatures = getUserInputFeatures(featuresList, featureNameMapping)
        df = getDataframeFromJson(request.session['dataframe'])

        if request.method == "POST":
            form = PreprocessingDataForm(request.POST, features=userInputFeatures)
            if form.is_valid():
                try:
                    formFields = []
                    for feature in userInputFeatures:
                        featureType = form.cleaned_data.get('%s_featureType' % feature)
                        dataType = form.cleaned_data.get('%s_dataType' % feature)
                        formFields.append(PreprocessingFormField(feature, featureType, dataType))

                    # Validate that the preprocessing input matches the data
                    validPreprocessingInput, errorMessages = validatePreprocessingInput(formFields, df)
                    if validPreprocessingInput:
                        request.session['formFields'] = [formField.to_JSON() for formField in formFields]
                        return redirect('preprocessing_confirmation')
                    else:
                        for errorMessage in errorMessages:
                            messages.warning(request, errorMessage)
                except Exception as e:
                    messages.warning(request, e)
        else: # GET
            form = PreprocessingDataForm(features=userInputFeatures)

        context = {
            'form': form,
        }
        return render(request, 'preprocessing/data_preprocessing.html', context)

    messages.warning(request, Messages.MISSING_SALES_DATA)
    return redirect('create_model')

def preprocessingConfirmation(request):
    if ('featuresList' in request.session
            and 'featureNameMapping' in request.session
            and 'dataframe' in request.session
            and 'formFields' in request.session):
        try:
            featureNameMapping = request.session['featureNameMapping']
            df = getDataframeFromJson(request.session['dataframe'])
            formFields = [as_PreprocessingFormField(json.loads(formField)) for formField in request.session['formFields']]

            #Success
            successColHeader = featureNameMapping['success']
            # We assume that the larger value is 'success', and the smaller value is 'failure'
            successValues, successValueCounts = getCategoriesAndCounts(df, successColHeader)

            #Salespeople
            salespeopleColHeader = featureNameMapping['salesperson id']
            salespeopleIds, salespeopleIdCounts = getCategoriesAndCounts(df, salespeopleColHeader)

            #Clients
            clientColHeader = featureNameMapping['client id']
            clientIds, clientCounts = getCategoriesAndCounts(df, clientColHeader)

            userInputFieldConfirmations = getUserInputFieldConfirmations(formFields, df)

            context = {
                'numRows': df.shape[0],
                'numDataCols': df.shape[1],
                'numSuccesses': df[successColHeader].value_counts()[successValues[1]],
                'numFailures': df[successColHeader].value_counts()[successValues[0]],
                'numSalespeople': len(salespeopleIds),
                'numClients': len(clientIds),
                'userInputFieldConfirmations': userInputFieldConfirmations,
            }
            return render(request, 'preprocessing/preprocessing_confirmation.html', context)
        except Exception as e:
            # Redirect to 'data_preprocessing' if there is an internal error
            raise e
            messages.warning(request, e)
            return redirect('data_preprocessing')

    messages.warning(request, Messages.MISSING_SALES_DATA)
    return redirect('create_model')

def loadingPage(request):
    return render(request, 'preprocessing/loading_page.html')

def modelResults(request):
    if ('featuresList' in request.session
            and 'featureNameMapping' in request.session
            and 'dataframe' in request.session
            and 'formFields' in request.session):
        try:
            featureNameMapping = request.session['featureNameMapping']
            df = getDataframeFromJson(request.session['dataframe'])
            formFields = [as_PreprocessingFormField(json.loads(formField))
                          for formField in request.session['formFields']]

            # Get required column headers
            successColHeader = featureNameMapping['success']
            salespeopleColHeader = featureNameMapping['salesperson id']
            clientColHeader = featureNameMapping['client id']

            modified_df, preprocessingSteps = preprocessDf(df,
                                                           salespeopleColHeader,
                                                           formFields)
            accuracy, modifiedDfFeatureCols = buildModel(modified_df, successColHeader, clientColHeader)

            request.session['preprocessingSteps'] = {k: v.to_JSON() for k, v in preprocessingSteps.items()}
            request.session['modifiedDfFeatureCols'] = modifiedDfFeatureCols
            context = {
                'accuracy': "{:.2%}".format(accuracy),
                'preprocessingSteps': preprocessingSteps,
            }
            #return HttpResponse(modified_df.sort_values(['Client ID'], ascending=[1]).to_html())
            return render(request, 'preprocessing/model_results.html', context)
        except Exception as e:
            # Redirect to 'data_preprocessing' if there is an internal error
            messages.warning(request, e)
            return redirect('data_preprocessing')

    messages.warning(request, Messages.MISSING_SALES_DATA)
    return redirect('create_model')
