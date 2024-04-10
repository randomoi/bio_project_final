"""
URL configuration for bioscience project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from bioscience_app import views
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from bioscience_app import views_api
from django.contrib import admin
from bioscience_app.views_api import CreateNewProteinView, RetrieveProteinByIDView, RetrievePfamDetailsView
from bioscience_app.views_protein import new_protein_form_page


from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from django.contrib import admin

# START: I wrote the code based on documentation and references. Important links were included in the comments next to each function. 
# Please review links below and short commentary in readme.txt. Thank you.

# creating schema for Swagger and ReDoc
schema = get_schema_view(
    openapi.Info(
        title="Bioscience Research Project",
        default_version="v1",
        description="The Bioscience Research project was designed and built for researchers to simplify 1) data retrieval and 2) creation of a new protein through RESTful web service.",
    ),
    public=True,
)

urlpatterns = [
    # swagger and redoc urls
    path('api/swagger/', schema.with_ui('swagger', cache_timeout=0), name='swagger'),
    path('api/redoc/', schema.with_ui('redoc', cache_timeout=0), name='redoc'),
    path('accounts/', include('django.contrib.auth.urls')),

    # rest of the project urls
    path('api/protein/', views_api.CreateNewProteinView.as_view(), name='protein-list'),
    path('api/protein/<str:protein_id>/', views_api.RetrieveProteinByIDView.as_view(), name='protein-detail'),
    path('api/pfam/<str:domain_id>/', views_api.RetrievePfamDetailsView.as_view(), name='pfam-domain-detail'),
    path('api/proteins/<int:taxa_id>/', views_api.ListProteinByTaxaView.as_view(), name='protein_by_taxa'),
    path('api/pfams/<int:taxa_id>/', views_api.ListDomainByTaxaView.as_view(), name='domain_by_taxa'),
    path('api/coverage/<str:protein_id>/', views_api.CoverageView.as_view(), name='coverage'),
    path('admin/', admin.site.urls),
    path('', include('bioscience_app.urls')),
    path('protein/create_new_protein/', new_protein_form_page, name='new_protein_form_page'),
]

# https://docs.djangoproject.com/en/3.2/howto/static-files/#serving-favicon-ico
if settings.DEBUG:
    urlpatterns += static('/favicon.ico', document_root=settings.STATIC_ROOT)

# END: I wrote the code based on documentation and references. Important links were included in the comments next to each function. 
# Please review links below and short commentary in readme.txt. Thank you.