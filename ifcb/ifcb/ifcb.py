#!/usr/bin/env python


import json
import argparse
import sys
from color import Text
import browser



# Print logo
def logo(logo_num, fg="fg_default", bg="bg_default", bright=True):
    
    logo = Text('''
╦╔═╗╔═╗╔╗   ╔═╗╔═╗╦
║╠╣ ║  ╠╩╗  ╠═╣╠═╝║
╩╚  ╚═╝╚═╝  ╩ ╩╩  ╩
''')

    if logo_num == 2:
        logo = Text('''
 _____ ______ _____ ____             _____ _____ 
|_   _|  ____/ ____|  _ \      /\   |  __ \_   _|
  | | | |__ | |    | |_) |    /  \  | |__) || |  
  | | |  __|| |    |  _ <    / /\ \ |  ___/ | |  
 _| |_| |   | |____| |_) |  / ____ \| |    _| |_ 
|_____|_|    \_____|____/  /_/    \_\_|   |_____|
                                                 ''')
    
    return logo.color(fg_color = fg, bg_color = bg, bright = bright)



# Accept command line arguments
def run_cmd_line():
    parser = argparse.ArgumentParser(
        description = 'Command-line api for accessing data in Imaging FlowCytobot database (WHOI-Plankton)'
    )

    parser.add_argument('-l', '--list',
                        action = 'store_true',
                        help = 'list all available datasets in IFCB database')

    parser.add_argument('-n', '--name',
                        metavar = 'dataset',
                        help = 'name of dataset to use')

    parser.add_argument('-s', '--start',
                        metavar = 'date',
                        help = 'start date for data collection')
    
    parser.add_argument('-e', '--end',
                        metavar = 'date',
                        help = 'end date for data collection')
    
    parser.add_argument('-i', '--instrument',
                        metavar = 'instrument',
                        help = 'name of instrument used')

    return parser



# Get list of all available datasets in IFCB database
def list_datasets():
    with open('datasets.json', 'r') as f:
        datasets = json.load(f)
    return datasets



def get_dataset(dataset_name, start_date=None, end_date=None):
    # Check if specified dataset exists
    datasets = list_datasets()
    if not dataset_name in datasets:
        print(f'No dataset named \'{dataset_name}\'', file=sys.stderr)
        print('Run \'ifcb -l\' to see the list of all available datasets')
        return (False, None)
    
    browser.get_data(dataset_name, start_date, end_date)
    

    return (True, True)
    

#def download_data()

def main():

    # Print logo
    print(logo(2, 'fg_green'))

    # Process command line arguments
    parser = run_cmd_line()
    args = parser.parse_args()

    # List available datasets
    if args.list:
        datasets = list_datasets()
        for dataset in datasets:
            print(dataset)
        sys.exit(0)
    
    # Get dataset, start date, end date
    if args.name is not None:
        pass
    # Get start date
    # if args.start is not None:

    # Get end date
    # if args.end is not None:

    sys.exit(0)



if __name__ == '__main__':
    main()
