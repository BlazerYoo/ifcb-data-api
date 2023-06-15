#!/usr/bin/env python


import json
import requests
import sys


def list_datasets():
    with open('datasets.json', 'r') as f:
        datasets = json.load(f)
    return datasets


def get_dataset(dataset_name):

    # Check if specified dataset exists
    datasets = list_datasets()
    if not dataset_name in datasets:
        print(f'No dataset named {dataset_name}', file=sys.stderr)
        return (False, None)
    
    url = f'https://ifcb-data.whoi.edu/timeline?dataset={dataset_name}'
    response = requests.get(url)
    if response.status_code == 200:
        # The request was successful
        content = response.content
        return (True, content)
    else:
        # The request failed
        print(f'Request failed with status code {response.status_code}', file=sys.stderr)
        return (False, None)

def download_data()

def main():
    print(list_datasets())

    success, content = get_dataset('mvco')
    if success:
        with open('asdf.html', 'wb') as f:
            f.write(content)

if __name__ == '__main__':
    main()