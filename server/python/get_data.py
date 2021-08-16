import requests
from datetime import date, timedelta
import os, csv, json
import pandas as pd
# current_date = format(date.today(), "%m-%d-%y")
def daily_report(report_date):
    formatted_date = report_date.format("%m-%d-%y")
    url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/3eaccd9f5ac8f0ab66b03e43e0bfdb8bbf8cc947/csse_covid_19_data/csse_covid_19_daily_reports/' + formatted_date +'.csv'
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
    data[-1] = []
    with open(tmpcsv,'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if (row['Country_Region'] == 'US'):
                fips = row['FIPS']
                value = dict(row.items())
                if (fips == ''):
                    key = -1 #data[-1].append(row.items())
                else:
                    key = int(row['FIPS'])
                # value = dict(row.items())
                # del value['FIPS']
                data[key]= value
                # print(row['FIPS'], row['Admin2'], row['Province_State'], row['Deaths'])
    jsonData = json.dumps(data, sort_keys=True)
    with open(tmpjson,'w', newline='') as jsonfile:
        jsonfile.write(jsonData)
    #df = pd.DataFrame(jsonData,columns=['Deaths', 'Province_State', 'Admin2'])
    #print(df)
    return pd.read_csv(tmpcsv)

if __name__ == '__main__':
    today = date.today()
    yesterday = format(today-timedelta(days=1),"%m-%d-%Y")
    df = daily_report(yesterday)
    #df = pd.DataFrame.from_dict(data,orient='index')
