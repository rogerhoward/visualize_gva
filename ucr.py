#!/usr/bin/env python
import os, sys
import requests
import simplejson as json
from pprint import pprint
import csv

path = 'ucr_crime_1975_2015.csv'
city_code = 'CA01941'
delete_fields = []

 # {'ORI': 'VA12800',
 #  'agg_ass_per_100k': '51.6787876244763',
 #  'agg_ass_sum': '234',
 #  'department_name': 'Virginia Beach, Va.',
 #  'homs_per_100k': '4.19614087549167',
 #  'homs_sum': '19',
 #  'months_reported': 'NA',
 #  'rape_per_100k': '22.7475005355601',
 #  'rape_sum': '103',
 #  'rob_per_100k': '59.6293703359342',
 #  'rob_sum': '270',
 #  'source': 'Crime in the U.S. 2015',
 #  'total_pop': '452797',
 #  'url': 'https://ucr.fbi.gov/crime-in-the-u.s/2015/crime-in-the-u.s.-2015/tables/table-8/table_8_offenses_known_to_law_enforcement_by_state_by_city_2015.xls',
 #  'violent_crime': '626',
 #  'violent_per_100k': '138.251799371462',
 #  'year': '2015'},

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

    data['aggravated_assaults'] = get_num(record.get('agg_ass_sum', -1))
    data['homicides'] = get_num(record.get('homs_sum', -1))
    data['rapes'] = get_num(record.get('rape_sum', -1))
    data['robberies'] = get_num(record.get('rob_sum', -1))
    data['population'] = get_num(record.get('total_pop', -1))
    data['violent_crime'] = get_num(record.get('violent_crime', -1))
    data['year'] = get_num(record.get('year', -1))


    return data

def get_ucr_for_city(city_code):
    print('Parsing UCR data...')

    with open(path, 'r') as f:
        data_list = list(csv.reader(f))
    record_list = [clean(dict(zip(data_list[0], x))) for x in data_list[1:]]
    filtered_list = [item for item in record_list if item['city_code'] == city_code]

    return filtered_list


twentysixteen = {'aggravated_assaults': 1481, 'homicides': 33, 'rapes': 197, 'robberies': 1138, 'population': 0, 'violent_crime': 2849}

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

        # record['data'].append(year[crime])

        record['data'].append(twentysixteen[crime])

        data['datasets'].append(record)

    pprint(data)
    return data

def save_ucr_data(records):
    print('Saving UCR data...')
    with open(data_path, 'w') as f:
        json.dump(records, f, indent=4, ensure_ascii=False, sort_keys=True)





if __name__ == "__main__":
    repo_path = os.path.dirname(os.path.realpath(sys.argv[0]))    # Path to current directory
    data_path = os.path.join(repo_path, 'data.json')                  # Root path for record data
    # os.makedirs(data_path, exist_ok=True)                         # Create _data directory

    years = get_ucr_for_city(city_code)                                      # Fetch UCR data and filter by city
    pprint(years)
    data = pivot_for_visualization(years)
    save_ucr_data(data)
