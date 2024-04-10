from django.views.generic import TemplateView
from django.shortcuts import render


# START: I wrote the code based on documentation and references. Important links were included in the comments next to each function. 
# Please review links below and short commentary in readme.txt. Thank you.

# https://docs.djangoproject.com/en/3.2/topics/http/shortcuts/#render
# https://docs.djangoproject.com/en/3.2/ref/class-based-views/base/#templateview

# request's and renders bioscience_app/spa.html
def SPA(request):
    return render(request, 'bioscience_app/spa.html')

# uses Django's TemplateView to produce a response
class IndexView(TemplateView):
    template_name = 'bioscience_app/spa.html'

# END: I wrote the code based on documentation and references. Important links were included in the comments next to each function. 
# Please review links below and short commentary in readme.txt. Thank you.