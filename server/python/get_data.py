import requests
from datetime import date, timedelta
import re
import os, csv, json
import pandas as pd
import pycountry
SERVER_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
TMP_DIR = os.path.join(SERVER_DIR, '_tmp')
TMP_CSV = os.path.join(TMP_DIR, 'tmp.csv')
# current_date = format(date.today(), "%m-%d-%y")
def download_csv(url,output_file=TMP_CSV):
    if ( not os.path.isdir(TMP_DIR)):
        os.mkdir(TMP_DIR)
    print(url) 
    r = requests.get(url)
    if (r.status_code != 200):
        raise Exception('404')
    else:
        text = r.text
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(text)
    return 1
def daily_report_us(report_date):
    formatted_date = report_date.format("%m-%d-%y")
    url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports_us/' + formatted_date +'.csv'
    csv_output = os.path.join(TMP_DIR, '{}.csv'.format(formatted_date))
    if (os.path.isfile(csv_output)):
        print('File {} is already downloaded'.format(csv_output))
    else:
        download_csv(url,output_file=csv_output)
    
    tmpjson = os.path.join(TMP_DIR,'{}.json'.format(formatted_date))
    data = {}
    print('Reading from csv')
    with open(csv_output,'r', encoding='utf-8', newline='\n') as csvfile:
        reader = csv.DictReader(csvfile)
        for rows in reader:
            key=rows['FIPS']
            data[key] = rows
    with open(tmpjson,'w', newline='') as jsonfile:
        jsonfile.write(json.dumps(data,indent=4,sort_keys=True))
    return pd.DataFrame(pd.read_csv(csv_output))
    # print(r.status_code)
    
def daily_report(report_date):
    formatted_date = report_date.format("%m-%d-%y")
    url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/' + formatted_date +'.csv'
    if ( not os.path.isdir(TMP_DIR)):
        os.mkdir(TMP_DIR)
    tmpcsv = os.path.join(TMP_DIR,'tmp.csv')
    tmpjson = os.path.join(TMP_DIR,'tmp.json')
    print(url)
    r = requests.get(url)
    if (r.status_code != 200):
        raise Exception('404')
        return 0
    print(r.status_code)
    text = r.text
    with open(tmpcsv, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)
        f.close()
        # writer = csv.writer(f)
        # writer.writerows(rows)
    data = {}
    # data[-1] = []
    j=-1
    with open(tmpcsv,'r', encoding='utf-8', newline='\n') as csvfile:
        reader = csv.DictReader(csvfile)
        for rows in reader:
            # if (row['Country_Region'] == 'US'):
            # value = dict(row.items())
            fips = rows['FIPS']
            if (fips != ''):
                key=int(fips)
                try:
                    (state_code, county_code) = re.search('^([\d]{,2})?([\d]{3})$', rows['FIPS']).groups()
                except:
                    print(fips, rows)
                    state_code = fips
                    county_code = 0
                rows.update( {'state_code':state_code, 'county_code': county_code} )
            else:
                #except ValueError:
                #print(rows['Country_Region'])

                try:
                    country = pycountry.countries.get(name=rows['Country_Region'])
                    if (country is None):
                        country = pycountry.countries.search_fuzzy(rows['Country_Region'])[0]
                    key = int(country.numeric)
                except (LookupError, AttributeError):
                    print('Unknown country:  {}'.format(rows['Country_Region']))
                    key = j
                    j -= 1

                # x =input('?')
                # print(rows)
                # x = input(' ')
                # key = j
                # j+=1
            # value = dict(row.items())
            # del value['FIPS']
            data[key] = rows
            # print(row['FIPS'], row['Admin2'], row['Province_State'], row['Deaths'])
    #return dat
    # return jsonData
    with open(tmpjson,'w', newline='') as jsonfile:
        jsonfile.write(json.dumps(data,indent=4,sort_keys=True))
    return data
    #df = pd.DataFrame(jsonData,columns=['Deaths', 'Province_State', 'Admin2'])
    #print(df)
    # return pd.read_csv(tmpcsv)

if __name__ == '__main__':
    today = date.today()
    yesterday = format(today-timedelta(days=1),"%m-%d-%Y")
    #df = daily_report(yesterday)
    us_df = daily_report_us(yesterday)
    
