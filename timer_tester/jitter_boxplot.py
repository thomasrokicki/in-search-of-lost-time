#!usr/bin/python3
''' Tools to create boxplot of the number of ticks per clock period on different versions.
This gives an indication of the evolution of the jitter.
The higher the average, the lower the resolution.
The larger the boxes, the higher the jitter.
'''
# Imports :
import json
import csv
import os
import statistics
import plotly.graph_objects as go
import sys
import argparse

# Locals:
import config
import utility


''' Reads data from all tested versions and return them in a buffer
You must first run client-side tests.

Parameters:
browser(str): Either 'chrome' or 'firefox'
coop(bool): Whether COOP/COEP is enabled (change values mainly for firefox)

Returns:
data(dict): The values of tick distribution for each version.
'''

def get_data(browser, coop):
    data = {}
    for file in os.listdir(config.RESULTS_DIR[browser]):
        path = config.RESULTS_DIR[browser] + file
        results = utility.read_json(path)
        for result in results:
            if result['name'] == 'Tick distibution' and result['coop'] == coop:
                print(result)

                data[result['version']] = result['values']
    return data



''' Plot the box graph of the number of ticks in a clock period.

Parameters:
browser(str): Either 'chrome' or 'firefox'
coop(bool): Whether COOP/COEP is enabled (change values mainly for firefox)
'''
def box_plot(browser, coop):
    data = get_data(browser,coop)
    if data == {}:
        print('No results found for ' + browser + ' with COOP/COEP: ' + str(coop))
    print(data)
    fig = go.Figure()
    for key in sorted(data.keys()):
        fig.add_trace(go.Box(y=data[key],name = key))
    fig.update_layout(
        paper_bgcolor='rgb(233,233,233)',
        plot_bgcolor='rgb(233,233,233)',
    )
    fig.show()

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--browser', help='Use a specific browser.', type=str, default='firefox')
    parser.add_argument('-c', '--coop', help = 'Use results with COOP and COEP. Default is off.', action='store_true',default=False)

    #parser.add_argument('--clean', help='Delete former result files. Default is false')
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    if sys.version_info < (3, 0):
        sys.stdout.write("Sorry, requires Python 3.x, not Python 2.x\n")
        sys.exit(1)
    args = parse_arguments()
    box_plot(args.browser,args.coop)
