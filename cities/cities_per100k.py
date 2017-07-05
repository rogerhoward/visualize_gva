#!/usr/bin/env python
import os, sys
import requests
import simplejson as json
from pprint import pprint
import csv

path = '../ucr_crime_1975_2015.csv'
delete_fields = []


def get_num(value):
    try:
        if value == 'NA':
            return -1
        elif '.' in value:
            return float(value)
        else:
            return int(value)
    except:
        return -1



def clean(record):
    data = {}
    data['city_code'] = record.get('ORI')
    data['city_name'] = record.get('department_name')
    data['aggravated_assaults'] = get_num(record.get('agg_ass_per_100k', -1))
    data['homicides'] = get_num(record.get('homs_per_100k', -1))
    data['rapes'] = get_num(record.get('rape_per_100k', -1))
    data['robberies'] = get_num(record.get('rob_per_100k', -1))
    data['population'] = get_num(record.get('total_pop', -1))
    data['violent_crime'] = get_num(record.get('violent_per_100k', -1))
    data['year'] = get_num(record.get('year', -1))

    return data


def get_ucr_for_city(city_code):
    print('Parsing UCR data...')

    with open(path, 'r') as f:
        data_list = list(csv.reader(f))
    record_list = [clean(dict(zip(data_list[0], x))) for x in data_list[1:]]
    filtered_list = [item for item in record_list if item['city_code'] == city_code]

    return filtered_list


def get_cities():
    print('Getting cities...')

    with open(path, 'r') as f:
        data_list = list(csv.reader(f))
        
    record_list = [clean(dict(zip(data_list[0], x))) for x in data_list[1:]]

    city_code_index = []
    cities = []
    for record in record_list:
        if record['city_code'] not in city_code_index:
            city_code_index.append(record['city_code'])
            cities.append({'name': record['city_name'], 'code': record['city_code']})

    return cities


def pivot_for_visualization(records, scale=False):
    labels = [str(x['year']) for x in records]
    labels.append('2016')

    data = {'labels': labels, 'datasets': []}
    colors = {'aggravated_assaults': (0, 51, 204), 'homicides': (153, 0, 204), 'rapes': (204, 0, 153), 'robberies': (10, 71, 255), 'population': (204, 0, 51), 'violent_crime': (0, 204, 153)}

    for crime in ['aggravated_assaults', 'homicides', 'rapes', 'robberies', 'violent_crime']:
        
        record = {"fill": False, "lineTension": 0.1, "backgroundColor": "rgba({},{},{},0.4)".format(*colors[crime]), "borderColor": "rgba({},{},{},1)".format(*colors[crime]), "borderCapStyle": "butt", "borderDash": [], "borderDashOffset": 0.0, "borderJoinStyle": "miter", "pointBorderColor": "rgba({},{},{},1)".format(*colors[crime]), "pointBackgroundColor": "#fff", "pointBorderWidth": 1, "pointHoverRadius": 5, "pointHoverBackgroundColor": "rgba({},{},{},1)".format(*colors[crime]), "pointHoverBorderColor": "rgba(220,220,220,1)", "pointHoverBorderWidth": 2, "pointRadius": 1, "pointHitRadius": 10, "spanGaps": False, "label": crime, "data": []}
        for year in records:
            if scale:
                record['data'].append(year[crime] / year['population'] * scale)
            else:
                record['data'].append(year[crime])

        data['datasets'].append(record)

    return data


def save_ucr_data(records, code):
    print('Saving UCR data...')
    file_name = '{}.json'.format(code)
    city_path = os.path.join(data_path, file_name)
    with open(city_path, 'w') as f:
        json.dump(records, f, indent=4, ensure_ascii=False, sort_keys=True)


def save_cities(cities):
    print('Saving city list...')
    file_name = 'cities.json'
    with open(file_name, 'w') as f:
        json.dump({'cities': cities}, f, indent=4, ensure_ascii=False, sort_keys=True)


if __name__ == "__main__":
    repo_path = os.path.dirname(os.path.realpath(sys.argv[0]))    # Path to current directory
    data_path = os.path.join(repo_path, 'data_per_100k')                  # Root path for record data
    os.makedirs(data_path, exist_ok=True)                         # Create _data directory

    cities = get_cities()                                      # Fetch UCR data and filter by city
    save_cities(cities)
    pprint(cities)

    for city in cities:
        pprint(city)
        years = get_ucr_for_city(city['code'])                                      # Fetch UCR data and filter by city
        data = pivot_for_visualization(years)
        save_ucr_data(data, city['code'])

 
    