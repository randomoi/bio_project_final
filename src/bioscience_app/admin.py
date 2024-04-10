from django.contrib import admin
from .models import Protein, Domain, Organism, Pfam, DomainAssignment

admin.site.register(Protein)
admin.site.register(Domain)
admin.site.register(Organism)
admin.site.register(Pfam)
admin.site.register(DomainAssignment)
