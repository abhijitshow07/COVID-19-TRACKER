# -*- coding: utf-8 -*-
"""
Created on Sun May 17 14:48:16 2020

@author: SAYAN GUHA ROY
"""


import json
import requests
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from fbprophet import Prophet
import math
import time
import calendar
from datetime import date, datetime

def india_world_pred():
    
    plt.close('all')
    plt.rcParams.update({'figure.max_open_warning': 0})
    
    #**** INDIA ****

    response = requests.get("https://corona.lmao.ninja/v3/covid-19/historical/india?lastdays=all")
    india = json.loads(response.text)
    
    cases=[]
    deaths=[]
    rec=[]
    for i in india['timeline']:
        for j in india['timeline'][i].items():
            if i == 'cases':
                cases.append(j)
            elif i == 'deaths':
                deaths.append(j)
            else:
                rec.append(j)
    
    #creating dataframe in the structure acceptable by fb prophet            
    cases = pd.DataFrame(cases,columns = ['ds','y'])
    deaths = pd.DataFrame(deaths,columns = ['ds','y'])
    rec=pd.DataFrame(rec,columns = ['ds','y'])
    
    #modifying the time
    #year = (datetime.now()).strftime('%Y')
    dates_list = []
    for i in range(len(cases)):
        a = cases['ds'][i].split("/")
        b = a[1]+' '+calendar.month_abbr[int(a[0])]+' 20'+ a[2]
        dates_list.append(b)    
    dates_list = pd.DataFrame(dates_list,columns = ['Date'])
    
    #creating csv file for india
    original = pd.concat([dates_list['Date'],cases['y'],deaths['y'],rec['y']],
                         axis=1,sort=False)
    original.columns = ['Date','Cases','Deaths','Recoveries']
    original.to_csv("data/india_original.csv")
    
    #converting values to log
    cases['y'] = np.log(cases['y'])
    deaths['y'] = np.log(deaths['y'])
    rec['y'] = np.log(rec['y'])
    
    #replacing infinite values with 0
    for i in range(len(cases)):
        if math.isinf(cases['y'][i]):
            cases['y'][i]=0
        if math.isinf(deaths['y'][i]):
            deaths['y'][i]=0
        if math.isinf(rec['y'][i]):
            rec['y'][i]=0
    
    ###predicting cases using fb prophet        
    m = Prophet()
    m.add_seasonality(name='daily', period=40.5, fourier_order=5)
    m.fit(cases)
    future = m.make_future_dataframe(periods=7)
    # future.tail()
    forecast = m.predict(future)
    # forecast[['ds', 'yhat']].tail()
    
    #plotting the model and saving it for cases
    plot_locations = []
    fig = m.plot(forecast)
    location = "static/img/plot/india_plot_cases" + str(date.today()) + ".png"
    plot_locations = plot_locations + [location]
    fig.legend(("actual","fitted","80% confidence interval"),loc='center right',fontsize=10)
    plt.savefig(location,figsize=(15,7),dpi=250)
    
    fig = m.plot_components(forecast)
    location = "static/img/plot/india_components_cases" + str(date.today()) + ".png"
    plot_locations = plot_locations + [location]
    plt.savefig(location,figsize=(15,7),dpi=250)
    
    #final dataframe for cases
    final_cases = pd.DataFrame()
    final_cases['ds'] = forecast['ds']
    final_cases['y'] = np.exp(forecast['yhat'])
    final_cases = final_cases.iloc[(len(final_cases)-7):,:].reset_index()
    final_cases.drop(columns = 'index',inplace=True)
    
    ###predicting deaths using fb prophet model
    m = Prophet()
    m.add_seasonality(name='daily', period=40.5, fourier_order=5)
    m.fit(deaths)
    future = m.make_future_dataframe(periods=7)
    # future.tail()
    forecast = m.predict(future)
    # forecast[['ds', 'yhat']].tail()
    
    #plotting the model and saving it for deaths
    fig = m.plot(forecast)
    location = "static/img/plot/india_plot_deaths" + str(date.today()) + ".png"
    plot_locations = plot_locations + [location]
    fig.legend(("actual","fitted","80% confidence interval"),loc='center right',fontsize=10)
    plt.savefig(location,figsize=(15,7),dpi=250)
    
    fig = m.plot_components(forecast)
    location = "static/img/plot/india_component_deaths" + str(date.today()) + ".png"
    plot_locations = plot_locations + [location]
    plt.savefig(location,figsize=(15,7),dpi=250)
    
    #final dataframe for deaths
    final_deaths = pd.DataFrame()
    final_deaths['ds'] = forecast['ds']
    final_deaths['y'] = np.exp(forecast['yhat'])
    final_deaths = final_deaths.iloc[(len(final_deaths)-7):,:].reset_index()
    final_deaths.drop(columns = 'index',inplace = True)
    
    ###predicting recoveries using fb prophet model
    m = Prophet()
    m.add_seasonality(name='daily', period=40.5, fourier_order=5)
    m.fit(rec)
    future = m.make_future_dataframe(periods=7)
    # future.tail()
    forecast = m.predict(future)
    # forecast[['ds', 'yhat']].tail()
    
    #plotting the model and saving it for recoveries
    fig = m.plot(forecast)
    location = "static/img/plot/india_plot_recovered" + str(date.today()) + ".png"
    plot_locations = plot_locations + [location]
    fig.legend(("actual","fitted","80% confidence interval"),loc='center right',fontsize=10)
    plt.savefig(location,figsize=(15,7),dpi=250)
    
    fig = m.plot_components(forecast)
    location = "static/img/plot/india_component_recovered" + str(date.today()) + ".png"
    plot_locations = plot_locations + [location]
    plt.savefig(location,figsize=(15,7),dpi=250)
    
    #creating final dataframe for recoveries
    final_rec = pd.DataFrame()
    final_rec['ds'] = forecast['ds']
    final_rec['y'] = np.exp(forecast['yhat'])
    final_rec = final_rec.iloc[(len(final_rec)-7):,:].reset_index()
    final_rec.drop(columns = 'index',inplace = True)
    
    dates_list = []
    for i in range(len(final_cases)):
        c = final_cases['ds'][i].strftime("%m/%d/%Y")
        a = c.split("/")
        b = a[1]+' '+calendar.month_abbr[int(a[0])]+' '+ a[2]
        dates_list.append(b)    
    dates_list = pd.DataFrame(dates_list,columns = ['Date'])
    
    ###creating the csv for fitted values for India
    fitted = pd.concat([dates_list['Date'],final_cases['y'],final_deaths['y'],final_rec['y']],
                       axis=1,sort=False)
    fitted.columns = ['Date','Cases','Deaths','Recoveries']
    fitted.to_csv("data/india_fitted.csv")
    
    
    #**** WORLD ****
    
    
    url_cases = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
    url_death = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
    url_recovered = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"
    
    df_cases = pd.read_csv(url_cases)
    df_death = pd.read_csv(url_death)
    df_recovered = pd.read_csv(url_recovered)
    
    #creating dataframe for cases
    
    data_cases = df_cases.groupby(['Country/Region']).sum()
    data_deaths = df_death.groupby(['Country/Region']).sum()
    data_rec = df_recovered.groupby(['Country/Region']).sum()
    
    
    data_cases.drop(columns = ['Lat','Long'],inplace=True)
    data_deaths.drop(columns = ['Lat','Long'],inplace=True)
    data_rec.drop(columns = ['Lat','Long'],inplace=True)
    
    #year = (datetime.now()).strftime('%Y')
    
    values_cases=[]
    for (i,k) in zip(range(data_cases.shape[1]),data_cases.columns):
        s = 0
        for j in range(data_cases.shape[0]):
            s = s + data_cases.iloc[j][i]
        values_cases.append(( k , s ))
        
    values_deaths=[]
    for (i,k) in zip(range(data_deaths.shape[1]),data_deaths.columns):
        s = 0
        for j in range(data_deaths.shape[0]):
            s = s + data_deaths.iloc[j][i]
        values_deaths.append(( k , s ))
    
    values_rec=[]
    for (i,k) in zip(range(data_rec.shape[1]),data_rec.columns):
        s = 0
        for j in range(data_rec.shape[0]):
            s = s + data_rec.iloc[j][i]
        values_rec.append(( k , s ))
        
    cases = pd.DataFrame(values_cases,columns = ['ds','y'])
    deaths = pd.DataFrame(values_deaths,columns = ['ds','y'])
    rec = pd.DataFrame(values_rec,columns = ['ds','y'])
    
    cases_list = list(cases['y'])
    deaths_list = list(deaths['y'])
    rec_list = list(rec['y'])
    
    dates_list = []
    for i in range(len(cases)):
        a = cases['ds'][i].split("/")
        b = a[1]+' '+calendar.month_abbr[int(a[0])]+' 20'+ a[2]
        dates_list.append(b)    
    
    #creating csv for original data for world
    world_original = pd.DataFrame(list(zip(dates_list,cases_list,deaths_list,rec_list)),
                                  columns = ['Date','Total Confirmed','Total Deaths','Total Recoveries'])
    world_original.to_csv('data/world_original.csv')
                                                                                                  
    #predicting world cases
    m = Prophet()
    m.add_seasonality(name='daily', period=30.5, fourier_order=5)
    m.fit(cases)
    future = m.make_future_dataframe(periods=7)
    forecast = m.predict(future)
    forecast[['ds', 'yhat']]
    
    #plotting and saving figure for world cases
    fig = m.plot(forecast)
    location = "static/img/plot/world_plot_cases" + str(date.today()) + ".png"
    plot_locations = plot_locations + [location]
    fig.legend(("actual","fitted","80% confidence interval"),loc='center right',fontsize=10)
    plt.savefig(location,figsize=(15,7),dpi=250)
    
    fig = m.plot_components(forecast)
    location = "static/img/plot/world_component_cases" + str(date.today()) + ".png"
    plot_locations = plot_locations + [location]
    plt.savefig(location,figsize=(15,7),dpi=250)
    
    fitted_dates = []
    fitted_cases = []
    for i in range(len(forecast)):
        a = forecast['ds'][i].strftime('%d %b %Y')
        b = a.split(" ")
        c = b[0]+' '+b[1]+' '+b[2]
        fitted_dates.append(c)
        
        if forecast['yhat'][i]<0:
            d = 0
        else:
            d = forecast['yhat'][i]
        fitted_cases.append(d)
        
    
    #predicting world deaths
    m = Prophet()
    m.add_seasonality(name='daily', period=30.5, fourier_order=5)
    m.fit(deaths)
    future = m.make_future_dataframe(periods=7)
    # future.tail()
    forecast = m.predict(future)
    # forecast[['ds', 'yhat']].tail()
    
    #plotting and saving the figure for world deaths
    fig = m.plot(forecast)
    location = "static/img/plot/world_plot_deaths" + str(date.today()) + ".png"
    plot_locations = plot_locations + [location]
    fig.legend(("actual","fitted","80% confidence interval"),loc='center right',fontsize=10)
    plt.savefig(location,figsize=(15,7),dpi=250)
    
    fig = m.plot_components(forecast)
    location = "static/img/plot/world_component_deaths" + str(date.today()) + ".png"
    plot_locations = plot_locations + [location]
    plt.savefig(location,figsize=(15,7),dpi=250)
    
    fitted_deaths = []
    for i in range(len(forecast)):
        if forecast['yhat'][i]<0:
            d = 0
        else:
            d = forecast['yhat'][i]
        fitted_deaths.append(d)
        
    #predicting world recovery
    m = Prophet()
    m.add_seasonality(name='daily', period=30.5, fourier_order=5)
    m.fit(rec)
    future = m.make_future_dataframe(periods=7)
    # future.tail()
    forecast = m.predict(future)
    # forecast[['ds', 'yhat']].tail()
    
    #plotting and saving for world recoveries
    fig = m.plot(forecast)
    location = "static/img/plot/world_plot_recovered" + str(date.today()) + ".png"
    plot_locations = plot_locations + [location]
    fig.legend(("actual","fitted","80% confidence interval"),loc='center right',fontsize=10)
    plt.savefig(location,figsize=(15,7),dpi=250)
    
    fig = m.plot_components(forecast)
    location = "static/img/plot/world_component_recovered" + str(date.today()) + ".png"
    plot_locations = plot_locations + [location]
    plt.savefig(location,figsize=(15,7),dpi=250)
    
    fitted_rec = []
    for i in range(len(forecast)):
        if forecast['yhat'][i]<0:
            d = 0
        else:
            d = forecast['yhat'][i]
        fitted_rec.append(d)
    
    #creating the csv for fitted values for world
    world_fitted = pd.DataFrame(list(zip(fitted_dates,fitted_cases,fitted_deaths,fitted_rec)),
                                columns = ['Date','Total Confirmed','Total Deaths','Total Recoveries'])
    world_fitted = world_fitted.iloc[(len(world_fitted)-7):,:].reset_index()
    world_fitted.drop(columns = ['index'],inplace=True)
    
    world_fitted.to_csv('data/world_fitted.csv')
    
    with open('json_data/plot_locations.json', 'w') as json_file:
        json.dump(plot_locations, json_file)
    
def country_wise():
    url_cases = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
    url_death = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
    url_recovered = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"
    
    df_cases = pd.read_csv(url_cases)
    df_death = pd.read_csv(url_death)
    df_recovered = pd.read_csv(url_recovered)
    
    #year = (datetime.now()).strftime('%Y')
    
    data_cases = df_cases.groupby(['Country/Region']).sum()
    data_death = df_death.groupby(['Country/Region']).sum().reset_index()
    data_recovered = df_recovered.groupby(['Country/Region']).sum().reset_index()
    
    data_cases.drop(columns=['Lat','Long'],inplace=True)
    data_death.drop(columns=['Lat','Long'],inplace=True)
    data_recovered.drop(columns=['Lat','Long'],inplace=True)
    
    date = []
    for i in data_cases.columns:
        a = i.split('/')
        b = a[1]+ ' '+ calendar.month_abbr[int(a[0])] + ' 20'+ a[2]
        date.append(b)
    
    date.insert(0,'Country') 
    data_cases = data_cases.reset_index()

    X_cases = data_cases.iloc[:,:].values
    X_deaths = data_death.iloc[:,:].values
    X_rec = data_recovered.iloc[:,:].values
    
    new_cases = pd.DataFrame(X_cases,columns = [date])
    new_deaths = pd.DataFrame(X_deaths,columns = [date])
    new_rec = pd.DataFrame(X_rec,columns = [date])
    
    new_cases.to_csv('data/country_wise_cases.csv')
    new_deaths.to_csv('data/country_wise_deaths.csv')
    new_rec.to_csv('data/country_wise_recovered.csv')

def read_country_list():
    df = pd.read_csv("data/country_wise_cases.csv")
    country = list(df['Country'])
    return country           

def read_country_data(country_index):
    df_cases = pd.read_csv("data/country_wise_cases.csv")
    df_deaths = pd.read_csv("data/country_wise_deaths.csv")
    df_rec = pd.read_csv("data/country_wise_recovered.csv")
    
    cases = list(df_cases.iloc[country_index,:].values)[2:]
    deaths = list(df_deaths.iloc[country_index,:].values)[2:]
    rec = list(df_rec.iloc[country_index,:].values)[2:]
    dates = list(df_cases.columns)[2:]
    
    final = pd.DataFrame(list(zip(dates,cases,deaths,rec)),columns = ['Date','Total Confirmed','Total Deaths','Total Recovered'])
    final_dict={}
    cases_list=[]
    deaths_list=[]
    rec_list=[]
    for i in range(len(final)):
        cases_list.append({final['Date'][i]: int(final['Total Confirmed'][i])})
        deaths_list.append({final['Date'][i]: int(final['Total Deaths'][i])})
        rec_list.append({final['Date'][i]: int(final['Total Recovered'][i])})
    
    final_dict['country'] = df_cases['Country'][country_index]
    final_dict['cases'] = cases_list
    final_dict['deaths'] = deaths_list
    final_dict['recovered'] = rec_list
    return final_dict

def world_original():
    final = pd.read_csv("data/world_original.csv")
    final_dict={}
    cases_list=[]
    deaths_list=[]
    rec_list=[]
    for i in range(len(final)):
        cases_list.append({final['Date'][i]: int(final['Total Confirmed'][i])})
        deaths_list.append({final['Date'][i]: int(final['Total Deaths'][i])})
        rec_list.append({final['Date'][i]: int(final['Total Recoveries'][i])})
    
    final_dict['cases'] = cases_list
    final_dict['deaths'] = deaths_list
    final_dict['recovered'] = rec_list
    return final_dict

def world_fitted():
    final = pd.read_csv("data/world_fitted.csv")
    final_dict={}
    cases_list=[]
    deaths_list=[]
    rec_list=[]
    for i in range(len(final)):
        cases_list.append({final['Date'][i]: int(final['Total Confirmed'][i])})
        deaths_list.append({final['Date'][i]: int(final['Total Deaths'][i])})
        rec_list.append({final['Date'][i]: int(final['Total Recoveries'][i])})
    
    final_dict['cases'] = cases_list
    final_dict['deaths'] = deaths_list
    final_dict['recovered'] = rec_list
    
    with open('json_data/plot_locations.json') as file:
        plot_locations = json.load(file)
        
    final_dict["plot_locations"] = plot_locations[6:13]
    
    return final_dict

def india_original():
    final = pd.read_csv("data/india_original.csv")
    final_dict={}
    cases_list=[]
    deaths_list=[]
    rec_list=[]
    for i in range(len(final)):
        cases_list.append({final['Date'][i]: int(final['Cases'][i])})
        deaths_list.append({final['Date'][i]: int(final['Deaths'][i])})
        rec_list.append({final['Date'][i]: int(final['Recoveries'][i])})
    
    final_dict['cases'] = cases_list
    final_dict['deaths'] = deaths_list
    final_dict['recovered'] = rec_list
    return final_dict

def india_fitted():
    final = pd.read_csv("data/india_fitted.csv")
    final_dict={}
    cases_list=[]
    deaths_list=[]
    rec_list=[]
    for i in range(len(final)):
        cases_list.append({final['Date'][i]: int(final['Cases'][i])})
        deaths_list.append({final['Date'][i]: int(final['Deaths'][i])})
        rec_list.append({final['Date'][i]: int(final['Recoveries'][i])})
    
    final_dict['cases'] = cases_list
    final_dict['deaths'] = deaths_list
    final_dict['recovered'] = rec_list
    
    with open('json_data/plot_locations.json') as file:
        plot_locations = json.load(file)
        
    final_dict["plot_locations"] = plot_locations[0:6]
    return final_dict

def india_daily_cumulative():
    statewise_daily = pd.read_csv("https://api.covid19india.org/csv/latest/state_wise_daily.csv")
    
    statewise_daily = statewise_daily.loc[statewise_daily["Status"] == 'Confirmed']
    statewise_daily.drop(['Date_YMD','TT','Status'], axis=1, inplace = True)
    statewise_daily.set_index(keys = "Date", inplace = True)
    
    statewise_daily = statewise_daily.cumsum()
    
    response = requests.get("https://api.covid19india.org/data.json")
    live = json.loads(response.text)
    state_codes={}
    for i in live["statewise"][1:]:
        state_codes[i['statecode']] = i['state']
    statewise_daily.rename(columns = state_codes, inplace = True)
    
    statewise_daily = statewise_daily.T
    statewise_daily.index.names = ['states']
    
    statewise_daily.to_csv('data/india_cumulative_cases.csv')

    
# https://api.covid19india.org/data.json
# https://api.covid19india.org/states_daily.json