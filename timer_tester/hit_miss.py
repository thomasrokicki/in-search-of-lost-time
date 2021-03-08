#!usr/bin/python3
''' Tools to create hit miss histogram, and get csv for latex
'''
# Imports :
import json
import csv
import os
import statistics
import plotly.graph_objects as go
import sys
import argparse
import math

# Locals:
import config
import utility



''' Write the csv file used to plot histogram in latex.

Parameters:
results(dict): Dictionnary indexed by timings, containing number of hits and misses for a certain timing.
output(string): Path of the output file.
'''
def hit_miss_csv(results,output):
    with open(output,'w') as file:
        writer = csv.writer(file,delimiter=' ')
        writer.writerow( ('timing', 'hit','miss') )
        for timing in results:
            writer.writerow( (timing, results[timing]['hits'],results[timing]['misses']) )

''' Computes the normalized histogram dict given a hit/miss distribution.

Parameters:
data(dict): Hit and Miss timings.
min_value(int): Minimal value in the computed histogram.
max_value(int): Maximal value in the computed histogram.
step(int): Bin size in the histogram.

Returns:
(dict) The histogram under the form of a dict indexed by timings.
'''
def get_histogram(data, min_value, max_value, step):
    results = {k: {'hits' : 0, 'misses' : 0} for k in range(min_value,max_value+step,step)}
    for hit in data['hits']:
        if hit<max_value and hit>min_value:
            results[hit//step*step]['hits'] += 1
    for miss in data['misses']:
        if miss<max_value and miss>min_value::
            results[miss//step*step]['misses'] += 1
    total = len(data['hits'])
    for key in results:
        results[key]['hits'] /= (total/100)
        results[key]['misses'] /= (total/100)
    return results


''' Plot the hit miss histogram.

Parameters:
data(dict): Hit and Miss timings.
min_value(int): Minimal value in the histogram.
max_value(int): Maximal value in the histogram.
step(int): Bin size in the histogram.
'''
def plot_hit_miss(data, min_value, max_value, step):
        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=data['hits'],
            name='hits',
            xbins=dict(
                start=min_value,
                end=max_value,
                size=step
            ),
        ))
        fig.add_trace(go.Histogram(
            x=data['misses'],
            name='misses',
            xbins=dict(
                start=min_value,
                end=max_value,
                size=step
            ),
        ))
        fig.layout.xaxis.update(range=[min_value,max_value])
        fig.show()



def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--browser', help='Use a specific browser.', type=str, default='firefox')
    parser.add_argument('-v', '--version', help='Use a specific version.', type=int, default=81)
    parser.add_argument('--clock', help='Use a specific clock method', type=str, default='performance.now')
    parser.add_argument('-c', '--coop', help = 'Use results with COOP and COEP. Default is off.', action='store_true',default=False)
    parser.add_argument('-p', '--plot', help = 'Plot hit/miss histogram', action='store_true',default=False)
    parser.add_argument('--csv', help = 'Create csv file (for latex)', action='store_true',default=False)
    parser.add_argument('--step', help = 'Step of the histogram', type=int, default = 1)
    parser.add_argument('--min', help = 'Min value of the histogram', type=int, default = 0)
    parser.add_argument('--max', help = 'Max value of the histogram', type=int, default = -1)

    #parser.add_argument('--clean', help='Delete former result files. Default is false')
    args = parser.parse_args()
    return args

def main(args):
    data = utility.read_json(config.RESULTS_DIR[args.browser] + args.browser + '-' + str(args.version) + '.json')
    (hits,misses) = ([],[])
    for result in data:
        if (result['name']=='hit/miss' and result['clock_method'] == args.clock and result['coop'] == args.coop):
            if result['hit/miss']=='hits':
                for value in result['values']:
                    hits.append(value)
            elif result['hit/miss']=='misses':
                for value in result['values']:
                    misses.append(value)
    if hits == [] or misses == []:
        print('No results found for ' + args.browser + ' ' + str(args.version) + ' ' + args.clock + ' and COOP/COEP:' +str(args.coop))
        sys.exit(1)
    results = {'hits':hits,'misses':misses}
    print(results)
    if args.csv:
        if args.max==-1:
            max_value= max(max(hits),max(misses))
        else:
            max_value = args.max
        hist = get_histogram(results, args.min, max_value, args.step)
        output_path = config.CSV_DIR[args.browser] + 'hit_miss-' + args.browser + '-' + str(args.version) + '-' + args.clock + '-coop-' + str(args.coop) + '.csv'
        hit_miss_csv(hist, output_path)
    if args.plot:
        if args.max==-1:
            max_value= max(max(hits),max(misses))
        else:
            max_value = args.max
        plot_hit_miss(results, args.min, max_value, args.step)



if __name__ == '__main__':
    if sys.version_info < (3, 0):
        sys.stdout.write("Sorry, requires Python 3.x, not Python 2.x\n")
        sys.exit(1)
    args = parse_arguments()
    main(args)
