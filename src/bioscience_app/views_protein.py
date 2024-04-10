import json
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from .models import Protein, Organism, Domain, Pfam
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import NewProteinForm, FormSetForDomainAssignment


# START: I wrote the code based on documentation and references. Important links were included in the comments next to each function. 
# Please review links below and short commentary in readme.txt. Thank you.

# https://docs.djangoproject.com/en/3.2/topics/http/shortcuts/#render
# https://docs.djangoproject.com/en/3.2/ref/contrib/messages/
# https://docs.djangoproject.com/en/3.2/ref/request-response/#django.http.HttpRequest.method
# https://docs.djangoproject.com/en/3.2/ref/forms/api/#django.forms.Form.is_valid
# https://docs.djangoproject.com/en/3.2/topics/forms/#the-save-method
# https://docs.djangoproject.com/en/3.2/ref/contrib/messages/#django.contrib.messages.success
# https://docs.djangoproject.com/en/3.2/ref/contrib/messages/#django.contrib.messages.error

# handles new protein creation from the form 
def new_protein_form_page(request):
    if request.method == 'POST': # checks if its a POST request 
        form = NewProteinForm(request.POST) # create new variable and add data from POST request
        if form.is_valid(): # validate form
            protein = form.save(commit=False) # save form without commit
            protein.save() # save protein to DB
            messages.success(request, 'Protein created successfully!') # show success message
            # refresh the page with blank fields
            return render(request, 'bioscience_app/create_new_protein.html', {'form': NewProteinForm(), 'success': True})
        else:
            # show error message
            messages.error(request, 'Failed to create protein. Please check the form data.')
    else:
        # if not POST request, create an empty form
        form = NewProteinForm()
    return render(request, 'bioscience_app/create_new_protein.html', {'form': form})

#  https://www.django-rest-framework.org/api-guide/exceptions/#validationerror
# handles data validation 
def data_validation(data):
    # required fields 
    protein_required_fields = ['protein_id', 'sequence', 'organism', 'length', 'domains']
    
    # if all required fields are not in the data raise an error
    if not all(field in data for field in protein_required_fields):
        raise ValidationError('Invalid data')
    
    # required fields 
    organism_required_fields = ['taxa_id', 'clade', 'genus', 'species']
    # if all required fields are not in the data raise an error
    if not all(field in data['organism'] for field in organism_required_fields):
        raise ValidationError('Invalid organism data')

    # loop over domain_data 
    for domain_data in data['domains']:
        # required fields 
        domain_required_fields = ['pfam_id', 'description', 'start', 'end']
        # if all required fields are not in the data raise an error
        if not all(field in domain_data for field in domain_required_fields):
            raise ValidationError('Invalid domain data')

        # required fields 
        pfam_required_fields = ['domain_id', 'domain_description']
        # if all required fields are not in the data raise an error
        if not all(field in domain_data['pfam_id'] for field in pfam_required_fields):
            raise ValidationError('Invalid pfam data')

# https://www.django-rest-framework.org/api-guide/exceptions/#validationerror
# https://docs.djangoproject.com/en/3.2/ref/models/querysets/#filter
# check if data exists for protein id, taxa id and domain id
def if_data_exists(data):
    # if protein with protein_id exists 
    if Protein.objects.filter(protein_id=data['protein_id']).exists():
        # if doesnt exist, raise an error
        raise ValidationError('Protein with this ID already exists')

    # if organism with taxa_id exists 
    if Organism.objects.filter(taxa_id=data['organism']['taxa_id']).exists():
        # if doesnt exist, raise an error
        raise ValidationError('Organism with this Taxa ID already exists')

    # go through domain data 
    for domain_data in data['domains']:
        # if Pfam with domain_id exists 
        if Pfam.objects.filter(domain_id=domain_data['pfam_id']['domain_id']).exists():
            # if doesnt exist, raise an error
            raise ValidationError('Pfam with this Domain ID already exists')


# https://docs.djangoproject.com/en/3.2/ref/csrf/#django.views.decorators.http.require_POST
# https://docs.djangoproject.com/en/3.2/ref/request-response/#jsonresponse-objects
# https://docs.python.org/3/library/json.html#json.loads
# https://docs.djangoproject.com/en/3.2/ref/models/querysets/#create
# https://www.django-rest-framework.org/api-guide/exceptions/#validationerror
# https://docs.djangoproject.com/en/3.2/ref/request-response/
# https://docs.djangoproject.com/en/3.2/ref/request-response/#jsonresponse-objects
# https://docs.djangoproject.com/en/3.2/topics/http/shortcuts/#redirect


# when create_new_protein URL is used this function is called
def create_new_protein(request):
    # confirm if POST request 
    if request.method == 'POST':
        # create form and add data from request 
        protein_form = NewProteinForm(request.POST)

        # form validation
        if protein_form.is_valid():
            # retrieve protein id from the form 
            protein_id = protein_form.cleaned_data.get('protein_id')

            # validate if protein with inouted protein id exists in DB
            if Protein.objects.filter(protein_id=protein_id).exists():
                # if exists, return 400 error with a JsonResponse error message 
                return JsonResponse({'error': 'Protein with this ID already exists'}, status=400)

            # if protein id doesnt exist, save form data as a new object
            protein = protein_form.save()

            # create a  variable and assign to it current protein object with data from request
            formset_domain_assignment = FormSetForDomainAssignment(request.POST, instance=protein)

            # validate if formset is valid
            if formset_domain_assignment.is_valid():
                # if valid, save as new Domain Assignment object
                formset_domain_assignment.save()
                # redirect to empty page
                return redirect('protein_list')
            else:
                # if invalid, delete created protein object
                protein.delete()

        # if invalid,eturn 400 error with a JsonResponse error message 
        return JsonResponse({'error': 'Failed to create protein. Please check the form data.'}, status=400)

    # if not POST request, create an empty form + formset
    else:
        protein_form = NewProteinForm()
        formset_domain_assignment = FormSetForDomainAssignment()

    # render the create_new_protein page with form + formset
    return render(request, 'bioscience_app/create_protein.html', {
        'protein_form': protein_form,
        'formset_domain_assignment': formset_domain_assignment,
    })

# END: I wrote the code based on documentation and references. Important links were included in the comments next to each function. 
# Please review links below and short commentary in readme.txt. Thank you.