from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from .forms import ContactForm
from django.contrib import messages
from django.conf import settings

def home(request):
    return render(request, 'base/home.html')


def welcome(request):
    return render(request, 'base/welcome.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                nameEmailMessage = "Full name: {} {}\nEmail: {}\n\n{}".format(first_name, last_name, from_email, message)
                send_mail(subject, nameEmailMessage, settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER])
                messages.success(request, 'Thank you for your message. We will get back to you shortly.')
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
