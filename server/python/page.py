#!/usr/bin/env python
# from lxml import etree
from django.template import Template, Context
from django.conf import settings
from datetime import date, timedelta
import pandas as pd
from get_data import daily_report
import django

settings.configure()
django.setup()
template = """<html>
<head>
<title>Template {{ target_date }}
</title>
</head>
<body>
<table>
<thead>
{% for k in data.keys %}
<th>{{k}}</th>
{% endfor %}
</thead>
<tbody>
{% for k,v in data.items %}
<tr>
<th>{{v}}</th>
<td>{{v}}</td>
</tr>
</tbody>
{% endfor %}


</table>
</body>
</html>
"""
def doRender(dat):
    # c = Context()
    return template.render(Context(dat))

# def main():
today = date.today()
for i in range(7):
    try:
        target_date = format(today-timedelta(days=i),"%m-%d-%Y")
        daily = daily_report(target_date)
    except Exception as e:
        print(e.args)
        if ('404' in e.args):
            continue
        else:
            break
    else:
        break

usDaily = daily.query('Country_Region == "US"')
di = pd.Index(daily.FIPS)

df = pd.DataFrame(usDaily.filter(['FIPS','Admin2','Province_State','Confirmed','Deaths','Case_Fatality_Ratio']).sort_values('Confirmed', ascending=False))
print(df)
