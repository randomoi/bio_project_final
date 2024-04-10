import datetime
from django import template
from django.shortcuts import render
from django import template

# START: I wrote the code based on documentation and references. Important links were included in the comments next to each function. 
# Please review links below and short commentary in readme.txt. Thank you.

# https://docs.python.org/3/library/datetime.html
# https://docs.djangoproject.com/en/3.2/howto/custom-template-tags/
# https://docs.djangoproject.com/en/3.2/howto/custom-template-tags/#registering-custom-filters-and-tags
# https://docs.djangoproject.com/en/3.2/howto/custom-template-tags/#simple-tags

register = template.Library()

# footer date tag
@register.simple_tag
def footer_date():
    return datetime.datetime.now().strftime("%d %b, %Y")

# copyright year tag
@register.simple_tag
def copyright_year():
   return datetime.datetime.now().year

# END: I wrote the code based on documentation and references. Important links were included in the comments next to each function. 
# Please review links below and short commentary in readme.txt. Thank you.
