#coding=utf-8
import numpy as np
import pandas as pd
import os
import re
import datetime as dt
from matplotlib.dates import date2num , DateFormatter
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.font_manager import FontProperties
font = FontProperties(fname=r"C:\\Windows\\Fonts\\simsun.ttc", size=25)
from mpl_toolkits.axes_grid1 import make_axes_locatable
import sys
sys.path.insert(1,r'H:\microwave_radiometer/')
import variables_dictionary as vd
from matplotlib.dates import DateFormatter
# vardic=vd.vardic

startime,endtime=['2020-04-01','2020-04-31']
# xticks=pd.date_range(start=startime,end=endtime,freq='D')


def create_empty_mother_array_for_dates_and_data(varname):
    dates_all=np.array([],dtype=int).reshape(0, 6) #### year,mon,day,hour,min,sec
    if vd.vardic[varname]['levels']!=None:
        levels=vd.vardic[varname]['levels']
        data_all=np.array([]).reshape(0,len(levels))
        # print levels
    if vd.vardic[varname]['levels']==None:
        data_all=np.array([]).reshape(0,1)
    return dates_all,data_all

# print xticks
# exit()
def draw_2D(varname,times,data_all):
    levels=vd.vardic[varname]['levels']
    xx,yy=np.meshgrid(times,levels)
    # print data_all.shape
    fig=plt.figure(figsize=(15,8))
    rect=0.1, 0.1, 0.7, 0.8
    ax=fig.add_axes(rect)        ### rect=l, b, w, h

    data_all=data_all.transpose()
    data_all = np.ma.masked_where(np.isnan(data_all),data_all)
    pcolormesh=ax.pcolormesh(xx,yy,data_all,cmap='coolwarm');

    fig.autofmt_xdate()
    ax.set_xticks(xticks)
    ax.xaxis.set_major_formatter(DateFormatter('%m-%d'))
    # ax.grid(True,axis='x')
    plt.xticks(rotation=90,ha='left')
    plt.title(unicode(varname,'utf-8')+'(%s)'%unicode(vd.vardic[varname]['unit'],'utf-8'),fontproperties=font)
    # xfmt = mdates.DateFormatter('%d %H:%M')
    # xfmt = mdates.DateFormatter('%m-%d')
    # ax.xaxis.set_major_formatter(xfmt)
    # ax.set_xlim(dt.datetime(2020,4,16,20,0,0),dt.datetime(2020,4,17,20,0,0))
    #### colorbar
    ax_colorbar=fig.add_axes([0.85,0.1,0.05,0.8])
    # ax_colorbar=fig.add_axes(rect=[0.85,0.1,0.1,0.8])
    fig.colorbar(mappable=pcolormesh,cax=ax_colorbar)

    plt.savefig(unicode(varname,'utf-8')+startime+'----'+endtime+'.png')
    plt.close()


def draw_1D(varname,times,data_all):
    # fig=plt.figure(figsize=(10,6))
    # rect=0.1, 0.1, 0.7, 0.8
    # ax=fig.add_axes(rect)
    fig,ax=plt.subplots(figsize=(15,12))

    fig.autofmt_xdate()
    # print times.shape,data_all.shape
    # ax.plot(times,data_all.transpose().flatten())
    # ax.scatter(times,data_all.transpose().flatten(),s=1)
    # times=times[::100]
    data=data_all.transpose().flatten()

    ax.plot_date(times,data,fmt='.')
    ax.set_xticks(xticks)
    ax.xaxis.set_major_formatter(DateFormatter('%m-%d'))
    ax.grid(True,axis='x')
    plt.xticks(rotation=90)
    plt.title(unicode(varname,'utf-8')+'(%s)'%unicode(vd.vardic[varname]['unit'],'utf-8'),fontproperties=font)
    # xfmt = mdates.DateFormatter('%m_%d, %H')
    # ax.xaxis.set_major_formatter(xfmt)
    # ax.set_xlim(dt.datetime(2020,4,16,20,0,0),dt.datetime(2020,4,17,20,0,0))
    # plt.show()

    plt.savefig(unicode(varname,'utf-8')+'.png')
    plt.close()

def draw_vardata_and_rain_2yaxis(varname,vardata,vardata_times,raindata,rain_times,xaxis=['202004162130','202004162300']):
    # fig=plt.figure(figsize=(10,6))
    fig, ax1 = plt.subplots(figsize=(15,9))
    ax2=ax1.twinx()
    levels=vd.vardic[varname]['levels'];
    if levels[-1]==10000:amplification_factor=20000
    if levels[-1]==2000:amplification_factor=20000/5
    # levels=np.array(levels)/1000.0
    # print levels
    # exit()
    xx,yy=np.meshgrid(vardata_times,levels)
    font = FontProperties(fname=r"C:\\Windows\\Fonts\\simsun.ttc", size=45)
    # plt.legend((a1,a2),('rain',unicode(varname,'utf-8')),prop=font)

    a2=ax1.pcolormesh(xx,yy, vardata.transpose(),label=unicode(varname,'utf-8'),cmap='coolwarm') #同上
    ax2.set_ylim(0,0.5)
    # a2=ax2.contourf(xx,yy, vardata.transpose()) #同上
    a1=ax1.plot(rain_times, np.array(raindata)*amplification_factor, c='blue',label='rain',linewidth=5) #绘制折线图像1,圆形点，标签，线宽
    # a1=ax1.scatter(rain_times, raindata,s=10, c='blue',label='rain') #绘制折线图像1,圆形点，标签，线宽
    fig.legend(loc=1,bbox_to_anchor=(1,1), bbox_transform=ax1.transAxes,prop=font)
    fig.autofmt_xdate()
    plt.xlim(dt.datetime.strptime(xaxis[0],'%Y%m%d%H%M'),
             dt.datetime.strptime(xaxis[1],'%Y%m%d%H%M'))

    ax1.tick_params(axis='x',labelsize=30,length=10,width=5)
    ax1.tick_params(axis='y',labelsize=30,colors='k')
    ax2.tick_params(axis='y',labelsize=20,colors='blue')

    ax1.grid(True,axis='x')
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    # divider = make_axes_locatable(ax1)
    # cax = divider.append_axes('bottom', size='5%', pad=0.1)
    plt.colorbar(mappable=a2)
    plt.tight_layout()
    plt.savefig(unicode(varname,'utf-8')+'_plus_rain'+'.png')

    plt.close()


### get hourly_rain data
hourlyrainfaile=open(r'2019june-2020june_hourly_rain.txt')
# station,rain_1h=np.loadtxt(r'2019june-2020june_hourly_rain111.txt',usecols=(9,10),skiprows=0,delimiter=',')
# print station,rain_1h
while True:
    line=hourlyrainfaile.readline()
    ss=line.split(',')
    # station=ss[5];year=ss[]
    year=ss[10];mon=ss[11];day=ss[12];hour=ss[13];rain_1h=ss[15]
    # print ss
    if line=='':
        break
        # print "fasdfasdfasdf"

exit()


ss={}
times_by_minute_dt_list=[]
# starttime_dt=dt.datetime(2020,05,01,00,00)
starttime_dt=dt.datetime.strptime(startime,'%Y-%m-%d')       #'2020-05-01' to datetime
endtime_dt=dt.datetime.strptime(endtime,'%Y-%m-%d')
while(starttime_dt<=endtime_dt+dt.timedelta(days=1)):
    times_by_minute_dt_list.append(starttime_dt)
    ss[starttime_dt]=np.full((53,1),np.nan)
    starttime_dt=starttime_dt+dt.timedelta(minutes=1)

# times_by_minute= np.array(times_by_minute)
#
# for i in times_by_minute:
#     ss[i]=np.full((53,1),np.nan)
from calendar import monthrange

# for varname in ['地面温度1B']:
for varname in ['水汽总含量']:
    if '廓线' not in varname:
        continue
    dd=ss
    if vd.vardic[varname]['filemark']=='L36000AMT':continue
    if varname=='俯仰2B':continue     ##### 所有值均为90.0;   多个分号
    print varname
    dates_all,data_all=create_empty_mother_array_for_dates_and_data(varname=varname)

    # for date in ['202004'+'%02d'%i for i in range(1,31)]:   ####to be corrected
    year=startime[:4];mon=startime[5:7];how_many_days=monthrange(int(year),int(mon))[-1]
    for date in [year+mon+'%02d'%i for i in range(1,how_many_days+1)]:   ####to be corrected
        print date
        if vd.get_dates_and_data(date=date,varname=varname)=="This date has no data":continue
        dates_array,data_array=vd.get_dates_and_data(date=date,varname=varname)
        if dates_array.shape[0]==0:continue
        # if dates_array==[]:
        #     print "Fasdfadfad"
        #     continue
        dates_all=np.concatenate([dates_all,dates_array])
        data_all=np.concatenate([data_all,data_array])
    # print dates_all
    # exit()
    # times=np.array([dt.datetime(i[0],i[1],i[2],i[3],i[4],i[5]) for i in dates_all])     #### xaxis
    times=np.array([dt.datetime(i[0],i[1],i[2],i[3],i[4]) for i in dates_all])     #### xaxis
    csv={}
    # print len(times)
    for i in range(len(times)):
        # print tuple(dates_all[i])
        csv[times[i]]=data_all[i,:]
    # print csv
    # exit()
    for time_dt in times:
        print time_dt
        # if time_dt not in ss.keys():print "vain time"
        dd[time_dt]=csv[time_dt]

    data=[]
    for time_dt in times_by_minute_dt_list:
        # print ss[time].shape
        data.append(dd[time_dt].reshape(53))
    data=np.array(data)
    # exit()
    print data.shape
    draw_2D(varname,times_by_minute_dt_list,data)
    # draw_1D(varname,times,data_all)
    # print times

    exit()