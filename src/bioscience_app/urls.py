from django.urls import path
from . import views
from .views_protein import new_protein_form_page
from .views import SPA, IndexView


# START: I wrote the code based on documentation and references. 
# Please review short commentary in readme.txt. Thank you.

urlpatterns = [
    path('spa/', SPA, name='spa'),
    path('', IndexView.as_view(), name='index'),
    path('protein/create_new_protein/', new_protein_form_page, name='new_protein_form_page'),
]

# END: I wrote the code based on documentation and references. 
# Please review short commentary in readme.txt. Thank you.