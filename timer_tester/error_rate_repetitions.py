#!usr/bin/python3
''' Tools to evaluate the impact of repetitions on a timer precision.
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


MAX_REP = 50


''' Computes the false hit rate.
That is, given a threshold that differentiates cache hits from cache misses,
the number of misses computed as hits.
For a standard clock, they are miss timings larger than the threshold.
However, as interpolation measure the time between the end of an operation and
the beginning of the next clock period, for interpolated clock they are miss
timings smaller than the threshold.

Parameters:
misses(list[int]): Miss timings.
threshold(int): Threshold to distinguish hits from misses.
clock_method(str): Used clock. We need it to take into account the difference for interpolated clocks.

Returns:
(int) The false hit rate as a proportion of total misses
'''
def get_false_hit_rate(misses,threshold, clock_method):
    false_hit_rate = 0
    for miss in misses:
        if clock_method == 'performance.now': # Interpolation makes everything backward :(
            if miss > threshold:
                false_hit_rate+=1
        elif clock_method == 'SharedArrayBuffer':
            if miss < threshold:
                false_hit_rate+=1
    return false_hit_rate/len(misses)

''' Computes the false miss rate.
That is, given a threshold that differentiates cache hits from cache misses,
the number of hits computed as misses.
For a standard clock, they are hit timings smaller than the threshold.
However, as interpolation measure the time between the end of an operation and
the beginning of the next clock period, for interpolated clock they are hit
timings larger than the threshold.

Parameters:
hits(list[int]): Hit timings.
threshold(int): Threshold to distinguish hits from misses.
clock_method(str): Used clock. We need it to take into account the difference for interpolated clocks.

Returns:
(int) The false miss rate as a proportion of total hits
'''
def get_false_miss_rate(hits,threshold, clock_method):
    false_miss_rate = 0
    for hit in hits:
        if clock_method == 'performance.now': # Interpolation makes everything backward :(
            if hit < threshold:
                false_miss_rate+=1
        elif clock_method == 'SharedArrayBuffer':
            if hit > threshold:
                false_miss_rate+=1
    return false_miss_rate / len(hits)



''' Computes the error rate for a given threshold.
That is the average of the false hit rate and the false miss rate.

Parameters:
hits(list[int]): Hit timings.
misses(list[int]): Miss timings.
threshold(int): Threshold to distinguish hits from misses.
clock_method(str): Used clock. We need it to take into account the difference for interpolated clocks.

Returns:
(int): The error rate as a proportion of total measurements.
'''
def get_error_rate(hits,misses, threshold,clock_method):
    return (get_false_hit_rate(misses, threshold, clock_method) + get_false_miss_rate(hits, threshold, clock_method))/2


''' Computes the best (lowest) error rate by testing different thresholds

Parameters:
hits(list[int]): Hit timings.
misses(list[int]): Miss timings.
clock_method(str): Used clock. We need it to take into account the difference for interpolated clocks.

Returns:
(int): The lowest error rate as a proportion of total measurements.
'''
def get_best_error_rate(hits, misses, clock_method):
    error_rate = []

    for threshold in range(0, math.floor(max(max(hits),max(misses)))):
        error_rate.append(get_error_rate(hits, misses, threshold, clock_method))

    return min(error_rate)


''' Get hit/miss timings with a certain number of repetitions
 To get repetition timings, we simply average different measurements.
 We do this in order to avoir recomputing hits and misses, as it is very time consuming.
A wiser attacker could exploit the distribution of the number of ticks in a clock
edge to get more information than just using average - but this was out of the scope.

Parameters:
hits(list[int]): Hit timings.
misses(list[int]): Miss timings.
measurement_reps(int): number of repetitions.

Returns:
(list,list): Lists of averaged hits/misses.
'''
def get_mean_rep(hits, misses, measurement_reps):
    hit_average = []
    miss_average = []
    for rep in range (0,len(hits),measurement_reps):
        hit_average.append(statistics.mean(hits[rep:rep+measurement_reps]))
        miss_average.append(statistics.mean(misses[rep:rep+measurement_reps]))
    return (hit_average,miss_average)

''' Computes the evolution of the hit/miss error rate for a specific situation.
For each repetition, we compute the lowest error rate.
This function reads data stored in the result folder.
This function can also output the result as a csv file or a graph.

Parameters:
browser(str): chrome or firefox.
version(int): studied version.
clock_method(str): What clock is used. Either SharedArrayBuffer or performance.now
coop(bool): True if coop/coep enabled.
csv(bool): Set to true if you wish to output the csv file.
plot(bool): Set to true if you wish to plot the evolution of error rate using plotly.
'''
def get_error_repetition(browser, version, clock_method, coop = False, csv = False, plot=False):
    results = utility.read_json(config.RESULTS_DIR[browser] + browser + '-' + str(version) + '.json')
    hits = []
    misses = []
    for result in results:
        if (result['name']=='hit/miss' and result['clock_method'] == clock_method and result['coop'] == coop):
            if result['hit/miss']=='hits':
                for value in result['values']:
                    hits.append(value)
            elif result['hit/miss']=='misses':
                for value in result['values']:
                    misses.append(value)
    if hits == [] or misses == []:
        print('No results found for ' + browser + ' ' + str(version) + ' ' + clock_method + ' and COOP/COEP:' +str(coop))
    error_rep = {}
    for rep in range(1, min(min(len(hits),len(misses)), MAX_REP)):
        (hit_avg, miss_avg) = get_mean_rep(hits,misses,rep)
        error_rep[rep] = get_best_error_rate(hit_avg,miss_avg, clock_method)
    if csv:
        output_path = config.CSV_DIR[browser] + 'error_rep-' + browser + '-' + str(version) + '-' + clock_method + '-coop-' + str(coop) + '.csv'
        json_to_csv(error_rep, output_path)
    if plot:
        plot_error_rep(error_rep)
    return(error_rep)

#                                   DISPLAY                                    #
def json_to_csv(error_rep, output):
    x = list(error_rep.keys())
    y = [error_rep[key] for key in x]
    with open(output,'w') as file:
        writer = csv.writer(file,delimiter=' ')
        writer.writerow( ('repetition','error_rate') )
        for key in error_rep.keys():
            writer.writerow( (key, error_rep[key]*100) )

def plot_error_rep(error_rep):
    x = list(error_rep.keys())
    y = [error_rep[key] for key in x]
    fig = go.Figure(data=go.Scatter(x=x, y=y))
    fig.show()


#                                     MAIN                                     #


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--browser', help='Use a specific browser.', type=str, default='firefox')
    parser.add_argument('-v', '--version', help='Use a specific version.', type=int, default=81)
    parser.add_argument('--clock', help='Use a specific clcok method', type=str, default='performance.now')
    parser.add_argument('-c', '--coop', help = 'Enables COOP and COEP. Default is off.', action='store_true',default=False)
    parser.add_argument('-p', '--plot', help = 'Plot error rate repetitions graph', action='store_true',default=False)
    parser.add_argument('--csv', help = 'Create csv file (for latex)', action='store_true',default=False)

    #parser.add_argument('--clean', help='Delete former result files. Default is false')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    if sys.version_info < (3, 0):
        sys.stdout.write("Sorry, requires Python 3.x, not Python 2.x\n")
        sys.exit(1)
    args = parse_arguments()
    get_error_repetition(args.browser, args.version, args.clock, coop = args.coop, csv = args.csv, plot = args.plot)
