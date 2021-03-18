import pandas as pd
import numpy as np
import sklearn as sk
import matplotlib.pyplot as plt
from sklearn import metrics
from json import *
import requests
pd.set_option('display.max_rows', 21000)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 150)



def read_csv():
    dataset = pd.read_csv('earthquakes.csv')
    return dataset


def concatener(dataset):
    dataset['Date_Time'] = dataset['Date'] + ' ' + dataset['Time']
    return dataset


def obtenir_type(dataset):
    return dataset['Type'].unique()


def obtenir_magnitude_type(dataset):
    return dataset['Magnitude Type'].unique()


def obtenir_status(dataset):
    return dataset['Status'].unique()


def obtenir_location_source(dataset):
    return dataset['Location Source'].unique()


def obtenir_magnitude_source(dataset):
    return dataset['Magnitude Source'].unique()


def convert_colonne(dataset):
    clean_convert = {'Type': {'Earthquake': 0, 'Nuclear Explosion': 1, 'Explosion': 2, 'Rock Burst': 3}}
    dataset = dataset.replace(clean_convert)
    return dataset


def moyenne_magnitude(dataset):
    return dataset['Magnitude'].mean()


def describe_magnitude(dataset):
    return dataset['Magnitude'].describe()


def convertir_time(dataset):
    dataset['Time_format_date'] = pd.to_datetime(dataset['Time'])
    return dataset

'''
def moyenne_time(dataset):
    dataset['Time_format_date'] = pd.to_datetime(dataset['Time_format_date']).values.astype(np.int64)

    dataset2 = pd.DataFrame(pd.to_datetime(dataset.groupby('column').mean().date))

    return dataset2['Time_format_date']
'''


def magnitude_nuclear_explosion(dataset):

    print(len(dataset[dataset['Type'] == 1].index))
    return dataset[dataset['Type'] == 1].describe()

'''
def magnitude_explosion(dataset):
    print(len(dataset[dataset['Type'] == 2].index))
    return dataset[dataset['Type'] == 2].describe()


def magnitude_rock_burst(dataset):
    print(len(dataset[dataset['Type'] == 3].index))
    return dataset[dataset['Type'] == 3].describe()
'''

def determiner_zone_pays(dataset):
    api_limit = 50
    api_start = 0
    tab_zone = []

    for index, row in dataset.iterrows():
        url = f'https://api.opencagedata.com/geocode/v1/json?q={row["Latitude"]}+{row["Longitude"]}&key=ba3304fd0ce3479c8f350eceb8c0a110'
        if api_start < api_limit:
            response = requests.get(url)
            geodata = loads(response.text)
        else:
            geodata = []
        country = None
        zone = None
        try:
            country = geodata['results'][0]['components']['county']
        except:
            pass
        try:
            country = geodata['results'][0]['components']['country']
        except:
            pass
        try:
            zone = geodata['results'][0]['components']['body_of_water']
        except:
            pass
        if country is not None:
            tab_zone.append(country)
        elif zone is not None:
            tab_zone.append(zone)
        else:
            tab_zone.append(None)
        api_start += 1
    dataset['zone'] = tab_zone


    return dataset

if __name__ == '__main__':
    dataset = read_csv()
    #print(dataset)
    print(obtenir_type(dataset))
    dataset2 = convert_colonne(dataset)
    #dataset2.to_csv('earthquakes2.csv')
    print(obtenir_magnitude_type(dataset2))
    print(obtenir_status(dataset2))
    #print(obtenir_location_source(dataset2))
    #print(obtenir_magnitude_source(dataset2))
    #print('moyenne magnitude ' + str(moyenne_magnitude(dataset2)))
    #print(describe_magnitude(dataset2))
    #print(dataset2)
    concatener(dataset2)

    dataset2.to_csv('earthquakes2.csv', index=False, header=dataset2.columns)
    #print(dataset2.columns)

    dataset3 = determiner_zone_pays(dataset2)
    dataset4 = convertir_time(dataset3)

    dataset4.to_csv('earthquakes3.csv', index=False, header=dataset4.columns)
    #print(moyenne_time(dataset4))
    print(magnitude_nuclear_explosion(dataset4))
    #print(magnitude_explosion(dataset4))
    #print(magnitude_rock_burst(dataset4))

    #ba3304fd0ce3479c8f350eceb8c0a110

