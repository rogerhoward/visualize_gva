#!/usr/bin/env python
import os, sys
import requests
import simplejson as json
from pprint import pprint
import csv

input_path = 'data.json'
output_path = 'diff.json'


def read_data():
    with open(input_path) as data_file:
        data = json.load(data_file)
    return data


def diff_data(input):
    output = []

    for i in range(0, len(input)):
        if i == 0:
            output.append(0)
        else:
            curr = input[i]
            last = input[i - 1]
            val = ((curr / last) - 1) * 100
            output.append(round(val, 2))

    return output


def diff_datasets(datasets):
    output = []
    for dataset in datasets:
        diffed_dataset = dict(dataset)
        diffed_dataset['data'] = diff_data(dataset['data'])
        print('-----')
        output.append(diffed_dataset)

    return output



def save_ucr_diff_data(records):
    print('Saving UCR data...')
    with open(output_path, 'w') as f:
        json.dump(records, f, indent=4, ensure_ascii=False, sort_keys=True)



if __name__ == "__main__":
    repo_path = os.path.dirname(os.path.realpath(sys.argv[0]))    # Path to current directory
    data_path = os.path.join(repo_path, 'data.json')                  # Root path for record data
    # os.makedirs(data_path, exist_ok=True)                         # Create _data directory

    data = read_data()
    pprint(data)


    print('--------------------------------------------------')

    dd = dict(data)
    dd['datasets'] = diff_datasets(data.get('datasets'))

    save_ucr_diff_data(dd)

    pprint(dd)