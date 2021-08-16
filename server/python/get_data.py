import requests
from datetime import date, timedelta
import os, csv, json
today = date.today()
yesterday = format(today-timedelta(days=1),"%m-%d-%Y")
# current_date = format(date.today(), "%m-%d-%y")
url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/3eaccd9f5ac8f0ab66b03e43e0bfdb8bbf8cc947/csse_covid_19_data/csse_covid_19_daily_reports/' + yesterday +'.csv'
serverdir = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
tmpdir = os.path.join(serverdir, '_tmp')
if ( not os.path.isdir(tmpdir)):
    os.mkdir(tmpdir)
tmpcsv = os.path.join(tmpdir,'tmp.csv')
tmpjson = os.path.join(tmpdir,'tmp.json')
print(url)
r = requests.get(url)
print(r.status_code)
text= r.text
with open(tmpcsv, 'w', newline='') as f:
    f.write(text)
    #writer = csv.writer(f)
    #writer.writerows(rows)
data = dict()
with open(tmpcsv,'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if (row['Country_Region'] == 'US'):
            key = row['FIPS']
            value = dict(row.items())
            del value['FIPS']
            data[key]= value
            # print(row['FIPS'], row['Admin2'], row['Province_State'], row['Deaths'])
jsonData = json.dumps(data, sort_keys=True)
with open(tmpcsv,'w', newline='') as jsonfile:
    jsonfile.write(jsonData)