from django import forms
from .models import Protein, Organism, Domain, Pfam, DomainAssignment
from django.forms.models import inlineformset_factory

# START: I wrote the code based on documentation and references. Important links were included in the comments next to each function. 
# Please review links below and short commentary in readme.txt. Thank you.

# https://docs.djangoproject.com/en/3.2/topics/forms/
# https://docs.djangoproject.com/en/3.2/topics/forms/modelforms/
# https://docs.djangoproject.com/en/3.2/ref/forms/validation/
# https://docs.djangoproject.com/en/3.2/ref/forms/fields/#modelmultiplechoicefield
# https://docs.djangoproject.com/en/3.2/topics/forms/modelforms/#inline-formsets
# https://docs.djangoproject.com/en/3.2/ref/models/instances/#django.db.models.Model.save
# https://docs.djangoproject.com/en/3.2/ref/models/querysets/
# https://www.djangoproject.com/community/q-and-a/?page=339

# organism form using Django's model
class FormForOrganism(forms.ModelForm):
    class Meta:
        model = Organism  # model used
        fields = '__all__'  # fields used


# new protein form using Django's model
class NewProteinForm(forms.ModelForm):
    class Meta:
        model = Protein  # model used
        fields = '__all__'  # fields used
    
    def clean_protein_id(self):
        protein_id = self.cleaned_data.get('protein_id')
        if Protein.objects.filter(protein_id=protein_id).exists():
            raise forms.ValidationError('Protein with this ID already exists.')
        return protein_id

# pfam form using Django's model
class FormForPfam(forms.ModelForm):
    class Meta:
        model = Pfam  # model used
        fields = '__all__'  # fields used


# domain form using Django's model
class FormForDomain(forms.ModelForm):
    class Meta:
        model = Domain  # model used
        fields = '__all__'  # fields used


# domain assignment form using Django's model
class FormForDomainAssignment(forms.ModelForm):
    class Meta:
        model = DomainAssignment  # model used
        fields = '__all__' # fields used


# extra = 1 form to show in formset
FormSetForDomainAssignment = inlineformset_factory(Protein, DomainAssignment, form=FormForDomainAssignment, extra=1)


# END: I wrote the code based on documentation and references. Important links were included in the comments next to each function. 
# Please review links below and short commentary in readme.txt. Thank you.