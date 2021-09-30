#!/usr/bin/env python
# from lxml import etree
import itertools
from django.template import Template, Context
from django.conf import settings
import matplotlib.pyplot as plt
from datetime import date, timedelta
import pandas as pd
from get_data import daily_report,daily_report_us
import django
import numpy as np

# def doRender(dat):
#     # c = Context()
#     return template.render(Context(dat))

# def main():
plt.style.use('classic')
today = date.today()
# for i in range(7):
#     try:
#         target_date = format(today-timedelta(days=i),"%m-%d-%Y")
#         daily = daily_report(target_date)
        
#     except Exception as e:
#         print(e.args)
#         if ('404' in e.args):
#             continue
#         else:
#             break
#     else:
#        break
for i in range(7):
    try:
        target_date = format(today-timedelta(days=i),"%m-%d-%Y")
        daily_us = daily_report_us(target_date)
        
    except Exception as e:
        print(e.args)
        if ('404' in e.args):
            continue
        else:
            break
    else:
        break



def label_bars(ax, heights, rects):
    """Attach a text label on top of each bar."""
    for height, rect in zip(heights, rects):
        ax.annotate(f'{height}',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 4),  # 4 points vertical offset.
                    textcoords='offset points',
                    ha='center', va='bottom')
# daily = daily_report(target_date)
#usDaily = daily.query('Country_Region == "US"')
# di = pd.Index(daily.FIPS)
print(daily_us)
df = daily_us.sort_values('Confirmed', na_position='last', ascending=False)
# df = daily_us.filter(['FIPS','Admin2','Province_State','Confirmed','Deaths','Case_Fatality_Ratio']).sort_values('Confirmed', ascending=False))
# print(df)
group_labels = ['Confirmed', 'Deaths', 'Case_Fatality_Ratio']
xlabels = df['Province_State']
# values = df.filter(xlabels).as_array()
k = df.filter(group_labels)
# k = list(map(lambda t: t[1], df.filter(xlabels).values()))
values = np.asarray(k).transpose() # [ *itertools.chain(k) ])
deaths = df['Deaths']
confirmed = df['Confirmed']
fig, ax = plt.subplots(nrows=3)

x = np.arange(values.shape[1])
# plt.plot(kind="bar")
# plt.figure();
for i in range(len(values)):
    ax[i].set_xticks(x)
    ax[i].set_xticklabels(xlabels,rotation=90)
    dimw = 0.75
    #for i in range(len(confirmed)):
    #    y = confirmed[i]
    # style = {'fill': False} if i == 0 else {'edgecolor': 'black'}
    b = ax[i].bar(x + i * dimw, values[i], dimw, bottom=0.0001)
    # label_bars(ax[i], values[i], b)
    # spacing = 0.2 # spacing between hat groups
    # width = (1 - spacing) / values.shape[0]
    # heights0 = values[0]
    # for i, (heights, group_label) in enumerate(zip(values, group_labels)):
    #     print(group_label,heights)
    #     style = {'fill': False} if i == 0 else {'edgecolor': 'black'}
    #     rects = ax.bar( x - spacing/2 + i * width, heights, width, bottom=0, label=group_label, align='edge', **style)
    #     label_bars(heights,rects)
    # x = np.linspace(0, len(df)+1, len(df))
    # fig = plt.figure()
    # ax[i].legend()


#b2 = ax[1].bar(x + i * dimw, deaths, dimw, bottom=0.0001)


# fig.tight_layout()
# ax2 = fig.add_subplot(211)
# ax2.set_xticks(x)
# ax2.set_xticklabels(xlabels,rotation=90)
# line = ax2.plot(x,df['Case_Fatality_Ratio'])
plt.show()
#ax1 = fig.add_subplot(211) 
#ax1.set_xlabel(df[''])
#ax1.bar(x, df['Confirmed'])
#ax1.bar(x, df['Deaths'])

# plt.show()