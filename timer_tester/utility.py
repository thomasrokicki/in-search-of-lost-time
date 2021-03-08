#!usr/bin/python3
import json
import statistics
import config
import os

def get_stats(timings, data=True):
    stats = {}
    if data:
        stats['values'] = timings
    stats['average'] = statistics.mean(timings)
    stats['standard_deviation'] = statistics.stdev(timings)
    stats['median'] = statistics.median(timings)
    return stats

def write_results(results, version, browser):
    if not os.path.exists(config.RESULTS_DIR[browser]):
        os.mkdir(config.RESULTS_DIR[browser])
    if browser in config.SUPPORTED_BROWSERS:
        path = config.RESULTS_DIR[browser] + browser + '-' + str(version) + '.json'
    else :
        raise Exception('Select a valid browser')
    try:
        with open(path,'r') as file:
            try:
                data = json.load(file)
            except json.decoder.JSONDecodeError as e:
                data = []
    except FileNotFoundError as e:
        data = []
    data.append(results)
    with open(path,'w') as file:
        json.dump(data,file,indent=4)

def read_json(path):
    with open(path,'r') as file:
        data = json.load(file)
    return data
