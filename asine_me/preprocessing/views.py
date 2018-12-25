from django.shortcuts import render, redirect
from .forms import UploadFileForm, PreprocessingDataForm
from .preprocessing_logic import getDfFromFile, getFeaturesFromDf, getJsonDataframe, preprocessDf, validateSalesData, getUserInputFeatures,getDataframeFromJson, getCategoriesAndCounts, buildModel
from django.contrib import messages

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

        if request.method == "POST":
            form = PreprocessingDataForm(request.POST, features=userInputFeatures)
            if form.is_valid():
                formFields = []
                for feature in userInputFeatures:
                    featureType = form.cleaned_data.get('%s_featureType' % feature)
                    dataType = form.cleaned_data.get('%s_dataType' % feature)
                    formFields.append({
                        'name': feature,
                        'featureType': featureType,
                        'dataType': dataType,
                    })
                request.session['formFields'] = formFields
                return redirect('preprocessing_confirmation')
        else: # GET
            form = PreprocessingDataForm(features=userInputFeatures)

        context = {
            'form': form,
        }
        return render(request, 'preprocessing/data_preprocessing.html', context)

    messages.warning(request, f'Please upload a sales data file and acknowledge the formatting rules first.')
    return redirect('create_model')


def loadingPage(request):
    return redirect('loading_page')


def preprocessingConfirmation(request):
    if ('featuresList' in request.session
            and 'featureNameMapping' in request.session
            and 'dataframe' in request.session
            and 'formFields' in request.session):
        featureNameMapping = request.session['featureNameMapping']
        df = getDataframeFromJson(request.session['dataframe'])
        formFields = request.session['formFields']

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

        userInputFieldConfirmations = []
        for formField in formFields:
            confirmation = {}
            confirmation['formField'] = formField
            colHeader = formField['name']

            if formField['featureType'] == 'Categorical':
                categories, categoryCounts = getCategoriesAndCounts(df, colHeader)
                confirmation['uniqueCategories'] = len(categories)
            elif formField['featureType'] == 'Numerical':
                confirmation['max'] = df.max(axis=0)[colHeader]
                confirmation['min'] = df.min(axis=0)[colHeader]
            elif formField['featureType'] == 'Boolean':
                categories, categoryCounts = getCategoriesAndCounts(df, colHeader)
                confirmation['uniqueCategories'] = len(categories)

            userInputFieldConfirmations.append(confirmation)

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

    messages.warning(request, f'Please upload a sales data file and acknowledge the formatting rules first.')
    return redirect('create_model')

def loadingPage(request):
    return render(request, 'preprocessing/loading_page.html')

def modelResults(request):
    if ('featuresList' in request.session
            and 'featureNameMapping' in request.session
            and 'dataframe' in request.session
            and 'formFields' in request.session):

        featureNameMapping = request.session['featureNameMapping']
        df = getDataframeFromJson(request.session['dataframe'])
        formFields = request.session['formFields']

        successColHeader = featureNameMapping['success']
        salespeopleColHeader = featureNameMapping['salesperson id']
        clientColHeader = featureNameMapping['client id']

        modified_df, preprocessingSteps = preprocessDf(df,
                                                       successColHeader,
                                                       salespeopleColHeader,
                                                       clientColHeader,
                                                       formFields)
        accuracy, featureCols = buildModel(modified_df, successColHeader, clientColHeader)

        request.session['preprocessingSteps'] = preprocessingSteps
        request.session['featureCols'] = featureCols
        context = {
            'accuracy': "{:.2%}".format(accuracy),
        }
        #return HttpResponse(modified_df.sort_values(['Client ID'], ascending=[1]).to_html())
        return render(request, 'preprocessing/model_results.html', context)

    messages.warning(request, f'Please upload a sales data file and acknowledge the formatting rules first.')
    return redirect('create_model')
