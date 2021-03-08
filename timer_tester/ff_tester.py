#!usr/bin/python3
''' This module contains most of the experiments related with Selenium on Firefox.
It uses the local server to run JS experiments.
You must start the server before running tests. See the server folder for more instructions.
You must first download browsers (see ./firefox/ff_downloader.py)

It can run the following tests :
    - Testing SharedArrayBuffer availablity.
    - Testing the number of incrementation in a clock period.
    - Retrieving timings for cache hits and misses.
    - Using RDTSC to evaluate timers.
'''

# Imports :
import json
from selenium import webdriver
from selenium.common.exceptions import JavascriptException, WebDriverException
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import subprocess
import os
import statistics
import plotly.graph_objects as go
import sys
import argparse
# Locals:
import config
import utility

#                                  SAB availablity                             #

def test_sab_flag(version, flags, coop = True):
    ''' Test the availablity of SABs for a certain set of flags.
    It logs to a certain page and check for the availability of SABs.

    Parameters:
    version(int): Tested version.
    flags(list): A list of Firefox starting preferences as strings.
    coop(bool): True to activate coop/coep, False otherwise.

    Returns:
    bool: the availablity of SABs with a specific set of flags
    '''
    fp = webdriver.FirefoxProfile()
    binary = FirefoxBinary(config.BROWSER_DIR['firefox'] + "firefox-" + str(version) + "/firefox")
    for (flag,value) in flags:
        fp.set_preference(flag, value)
    sab_available = False
    with (webdriver.Firefox(firefox_binary=binary, firefox_profile = fp)) as driver:
        if coop:
            url = config.URLS['hit_miss'] + "?coop=True"
        else:
            url = config.URLS['hit_miss']
        try:
            sab_available = (driver.execute_script("""if (SharedArrayBuffer=='undefined'){return 'False'} else{return 'True'}"""))
        except JavascriptException:
            return False # For version where sab where not implemented - versions where they are implemented and not disable don't throw exceptions.
        driver.close();
    return (sab_available=='True')



def test_sab(version, coop = True):
    ''' Perform the availablity checks for SABs by testing different sets of flags for a specific version.
    As long as no set works, we keep adding some.
    If no flag work, we abandon.
    Then writes in a file results: availablity, needed flags, is COOP/COEP enabled.

    Parameters:
    version(int): Tested version
    coop(bool): True to activate coop/coep, False otherwise.
    '''

    print('Testing the availability of SABS in a clock period on Firefox ' + str(version))
    if coop:
        print('COOP/COEP is on.')
    else:
        print('COOP/COEP is off.')
    sab_available = False # Flag for while loop, set to true when sabs are availables
    flag_dict= {'javascript.options.shared_memory': False,
            'dom.postMessage.sharedArrayBuffer.withCOOP_COEP': False,
            'browser.tabs.remote.useCrossOriginEmbedderPolicy': False,
            'browser.tabs.remote.useCrossOriginOpenerPolicy': False,
            }
    flags = [] # Store the needed flags
    while not sab_available: #As long as sab are unavailable, we keep adding. Might need to add potential new flags here.
        sab_available = test_sab_flag(version,flags, coop)

        if ((not sab_available) and (not flag_dict['javascript.options.shared_memory'])): # Flags for versions 58 and later, befor COOP/COEP
            print("Test of SharedArrayBuffer failed, trying with javascript.options.shared_memory")
            flags.append(('javascript.options.shared_memory', True))
            flag_dict['javascript.options.shared_memory'] = True

        elif ((not sab_available) and (not flag_dict['dom.postMessage.sharedArrayBuffer.withCOOP_COEP'])): #flag required after the implementation of coop/coep, but not their official release
            print("Test of SharedArrayBuffer failed, trying with dom.postMessage.sharedArrayBuffer.withCOOP_COEP")
            flags.append(('dom.postMessage.sharedArrayBuffer.withCOOP_COEP', True))
            flags.append(('browser.tabs.remote.useCrossOriginEmbedderPolicy', True))
            flags.append(('browser.tabs.remote.useCrossOriginOpenerPolicy', True))

            flag_dict['dom.postMessage.sharedArrayBuffer.withCOOP_COEP'] = True
            flag_dict['browser.tabs.remote.useCrossOriginEmbedderPolicy'] = True
            flag_dict['browser.tabs.remote.useCrossOriginOpenerPolicy'] = True

        else:
            break

    stats = {'name': 'SAB availablity',
             'sab_available': sab_available,
             'coop': coop,
             'version': version,
             'flags': flags
            }
    utility.write_results(stats, version, 'firefox')
    print("SharedArrayBuffer: " + str(sab_available) + " (Can require flags.)")
    print()




#                              TICK DISTRIBUTION                               #

def test_interpolation_distribution(version, coop = True, repetitions = config.REPETITIONS):
    ''' Test repeatedly the number of maximum incrementations in a clock edge.
    This gives indication of both resolution (average number of incrementations)
    and jitter (variance of the number of ticks).
    It also allows to plot the histogram of the distribution of the number of incrementations.
    Writes the result in the folder div.

    Parameters:
    version(int): Tested version
    coop(bool): True to activate coop/coep, False otherwise.
    repetitions(int): The number of measurements. Default is set in config file.
    '''

    print('Testing the number of ticks in a clock period on Firefox ' + str(version) + ", " + str(repetitions) + ' repetitions.')
    if coop:
        print('COOP/COEP is on.')
    else:
        print('COOP/COEP is off.')
    fp = webdriver.FirefoxProfile()
    binary = FirefoxBinary(config.BROWSER_DIR['firefox'] + "firefox-" + str(version) + "/firefox")
    with(webdriver.Firefox(firefox_binary=binary, firefox_profile = fp)) as driver:
        if coop:
            driver.get(config.URLS['distribution'] + "?coop=True")
        else:
            driver.get(config.URLS['distribution'])
        timings = driver.execute_script("return test_clock_edges(" + str(repetitions) + ")")
        driver.close();
    stats = utility.get_stats(timings)
    stats['name'] = 'Tick distibution'
    stats['version'] = version
    stats['coop'] = coop
    utility.write_results(stats, version, 'firefox')
    print('Done')
    print()

#                            CACHE HITS/MISSES                                 #
def test_hits_misses(version, clock_method, coop = True, repetitions = config.REPETITIONS):
    ''' Compute the access time of cache hits and misses for a specific clock.
    This method can take a while to run, especially with a lot of repetitions or
    a huge cache.
    Also note that running computations on the side will create a lot of noise,
    as the cache is shared by all processes.
    Timing measured by this measurement can be used to determine error rate as
    well as the impact of repetitions

    Parameters:
    version(int): Tested version
    clock_method(string): Which clock to use. Can be 'SharedArrayBuffer' or 'performance.now'.
    coop(bool): True to activate coop/coep, False otherwise.
    repetitions(int): The number of measurements. Default is set in config file.
    '''

    print('Testing hits/misses on Firefox ' + str(version) + " with " + clock_method + ", " + str(repetitions) + ' repetitions.')
    if coop:
        print('COOP/COEP is on.')
    else:
        print('COOP/COEP is off.')
    fp = webdriver.FirefoxProfile()
    binary = FirefoxBinary(config.BROWSER_DIR['firefox'] + "firefox-" + str(version) + "/firefox")
    with(webdriver.Firefox(firefox_binary=binary, firefox_profile = fp)) as driver:
        if coop:
            driver.get(config.URLS['hit_miss'] + "?coop=True")
        else:
            driver.get(config.URLS['hit_miss'])
        try:
            driver.set_script_timeout(10000000000)
            results = driver.execute_script("return getHitMiss('" + clock_method + "'," +  str(repetitions) + ")") #This might fail if SABs are unavailable so we set a try
        except JavascriptException as e: # This exception occurs when we try to access to SABs without coop/coep on later versions.
            print('SABs are not available without coop here, skipping')
            return
        except WebDriverException: # This exception occurs when SABs are disabled/not implemented, so mainly old versions.
            print('SABs are not available here, skipping')
            return
        driver.close();

    stat_hits = utility.get_stats(results['hits'])
    stat_hits['name'] = 'hit/miss'
    stat_hits['clock_method'] = clock_method
    stat_hits['hit/miss'] = 'hits'
    stat_hits['version'] = version
    stat_hits['coop'] = coop
    utility.write_results(stat_hits, version, 'firefox')

    stat_misses = utility.get_stats(results['misses'])
    stat_misses['name'] = 'hit/miss'
    stat_misses['clock_method'] = clock_method
    stat_misses['hit/miss'] = 'misses'
    stat_misses['version'] = version
    stat_misses['coop'] = coop
    utility.write_results(stat_misses, version, 'firefox')
    print('Done')
    print()

#                                 RDTSC                                        #
def test_rdtsc(coop = True, repetitions = config.REPETITIONS):
    ''' Measure the execution time of our timers.
    This needs a custom version of firefox where performance.rdtsc is implemented.
    Reference the executable in the config file.
    Writes the output in a different file than the other experiments.

    Parameters:
    coop(bool): True to activate coop/coep, False otherwise.
    repetitions(int): The number of measurements. Default is set in config file.
    '''
    print('Testing RDTSC')
    if not config.RDTSC_EXEC['firefox']:
        print('You have not defined the path to custom rdtsc Firefox.')
        print('Please set it up properly in the config file.')
        print('Skipping...')
        return
    results = {}
    fp = webdriver.FirefoxProfile()
    binary = FirefoxBinary(config.RDTSC_EXEC['firefox'])
    with(webdriver.Firefox(firefox_binary=binary, firefox_profile = fp)) as driver:
        if coop:
            driver.get(config.URLS['rdtsc'] + "?coop=True")
        else:
            driver.get(config.URLS['rdtsc'])
        driver.close();
    results['name'] = 'rdtsc'
    results['coop'] = coop
    utility.write_results(results, 'rdtsc', 'firefox')
    print('Done')
    print()

#                                  MAIN                                        #

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--version', help='Use a specific version. By default, runs all versions from 57 to latest.', type=int)
    parser.add_argument('-r', '--repetitions', help='Number of measurements for hit/miss, distribution and rdtsc.', type=int)
    parser.add_argument('-c', '--coop', help = 'Enables COOP and COEP. Default is off.', action='store_true',default=False)
    parser.add_argument('--sab', help='Run the availablity tests for SharedArrayBuffer.', action='store_true',default=False)
    parser.add_argument('--distribution', help='Evaluates the number of incrementation per clock period.', action='store_true',default=False)
    parser.add_argument('--hit_miss', help='Evaluates timings for cache hits and misses. This can take a while.', action='store_true',default=False)
    parser.add_argument('--rdtsc', help='Run performance.rdtsc tests. You need to set the path of you custom firefox in the config file.', action='store_true',default=False)

    #parser.add_argument('--clean', help='Delete former result files. Default is false')
    args = parser.parse_args()
    return args


def main(args):
    #clean = args.clean
    if args.repetitions:
        repetitions = args.repetitions
    else:
        print('You have not specified a number of repetitions. Using config.')
        repetitions = config.REPETITIONS
    print('Number of measurements : '+str(repetitions))

    if args.version:
        if args.version in config.ALL_VERSIONS['firefox'] and args.version >= 57:
            versions = [args.version]
        else:
            print('Only support versions later than 57')
            sys.exit(1)
    else:
        print('Running tests on all available versions.')
        print(config.ALL_VERSIONS['firefox'])
        versions = config.ALL_VERSIONS['firefox']

    if args.coop:
        print('Using coop for tests.')
        coop = True
    else:
        print('Not using coop for tests.')
        coop = False

    if args.rdtsc:
        print('a')
        test_rdtsc(coop = True, repetitions = config.REPETITIONS) # Since rdtsc does not require a version, we treat it differently - you can't run rdtsc and the others in the same run.
        #TODO: Maybe improve the CLI.
    else:
        print(args)
        if not ((args.sab) or (not args.hit_miss) or (args.distribution)):
            print("You have not specified tests, running sab availability, distribution and hit_miss")
            for version in versions:
                print("Evaluating version " + str(version))
                test_sab(version, coop)
                test_interpolation_distribution(version, coop, repetitions)
                test_hits_misses(version, 'SharedArrayBuffer', coop , repetitions)
                test_hits_misses(version, 'performance.now', coop , repetitions)
        else:
            print(args)
            if args.sab:
                for version in versions:
                    test_sab(version, coop)
            if args.distribution:
                for version in versions:
                    test_interpolation_distribution(version, coop, repetitions)
            if args.hit_miss:
                for version in versions:
                    test_hits_misses(version, 'SharedArrayBuffer', coop , repetitions)
                    test_hits_misses(version, 'performance.now', coop , repetitions)




if __name__ == '__main__':
    if sys.version_info < (3, 0):
        sys.stdout.write("Sorry, requires Python 3.x, not Python 2.x\n")
        sys.exit(1)
    args = parse_arguments()
    main(args)
