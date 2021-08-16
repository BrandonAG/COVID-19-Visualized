#!/usr/bin/env python
# from lxml import etree
from django.template import Template, Context
from django.conf import settings
from datetime import date, timedelta
import pandas as pd
from get_data import daily_report

today = date.today()
yesterday = format(today-timedelta(days=1),"%m-%d-%Y")
cdf = daily_report(yesterday)

# df = pd.DataFrame(data.items(),columns=['Province_State','Confirmed','Deaths','Active'])
# from django.template import engines
# settings.configure(TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [],
#         'APP_DIRS': False,
#         'OPTIONS': {
#             # ... some options here ...
#         },
#     },
# ]) # We have to do this to use django templates standalone - see
# # # http://stackoverflow.com/questions/98135/how-do-i-use-django-templates-without-the-rest-of-django

# # Our template. Could just as easily be stored in a separate file
# template = Template("My name is {{ my_name }}.")
#  """
# <html>
# <head>
# <title>Template {{ title }}</title>
# </head>
# <body>
# Body with {{ mystring }}.
# </body>
# </html>
# """
def doRender(dat):
# c = Context()
    return template.render(Context(dat))
# doRender({"title": "title from code", "mystring":"string from code", "my_name":"Patrick"})

