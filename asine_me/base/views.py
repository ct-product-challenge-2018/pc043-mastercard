from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from .forms import ContactForm
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect

def home(request):
    return render(request, 'base/home.html')

def welcome(request):
    return render(request, 'base/welcome.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email,
                          [])
                messages.success(request, 'Thank you for your message.')
                return redirect('asineme_home')
            except BadHeaderError:
                messages.warning(request, 'Invalid header.')
            except:
                messages.warning(request, 'Error sending mail.')
    else:
        form = ContactForm()

    context = {
        'form': form,
    }

    return render(request, "base/contact.html", context)